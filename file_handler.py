import os
import boto3
import logging
import importlib

from django.utils.text import slugify
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from django.utils import timezone
from django.core.files.uploadhandler import FileUploadHandler
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# Initialize Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django
django.setup()

def get_setting(name, default=None):
    return getattr(settings, f'CHUNK_UPLOADER_{name}', getattr(settings, name, default))

logger = logging.getLogger(__name__)

# Get AWS settings from Django settings
AWS_ACCESS_KEY_ID = get_setting('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_setting('AWS_SECRET_ACCESS_KEY')
AWS_REGION = get_setting('AWS_REGION', 'ap-south-1')
AWS_STORAGE_BUCKET_NAME = get_setting('AWS_STORAGE_BUCKET_NAME', 'monitor-app-v1')
S3_DOCUMENT_ROOT_DIRECTORY = get_setting('S3_DOCUMENT_ROOT_DIRECTORY', '')
S3_APPEND_DATETIME_ON_UPLOAD = get_setting('S3_APPEND_DATETIME_ON_UPLOAD', True)
S3_PREFIX_QUERY_PARAM_NAME = get_setting('S3_PREFIX_QUERY_PARAM_NAME', '__prefix')
S3_MIN_PART_SIZE = get_setting('S3_MIN_PART_SIZE', 5 * 1024 * 1024)
CLEAN_FILE_NAME = get_setting('CLEAN_FILE_NAME', False)
MAX_UPLOAD_SIZE = get_setting('MAX_UPLOAD_SIZE', None)
S3_ENDPOINT_URL = get_setting('AWS_S3_ENDPOINT_URL', None)
S3_GENERATE_OBJECT_KEY_FUNCTION = get_setting('S3_GENERATE_OBJECT_KEY_FUNCTION', None)
AWS_S3_FILE_BUFFER_SIZE = get_setting('AWS_S3_FILE_BUFFER_SIZE', 5242880)

# If a custom key generation function is provided, import it and prepare it for use
if S3_GENERATE_OBJECT_KEY_FUNCTION:
    func_parts = S3_GENERATE_OBJECT_KEY_FUNCTION.split('.')
    module = importlib.import_module('.'.join(func_parts[0:-1]))
    generate_object_key = getattr(module, func_parts[-1])
else:
    def generate_object_key(request, filename):
        filename_base, filename_ext = os.path.splitext(filename)
        _now_postfix = ''
        if S3_APPEND_DATETIME_ON_UPLOAD:
            _now_postfix = f'_{timezone.now().strftime("%Y%m%d%H%M%S")}'
        _filename = f'{filename_base}{_now_postfix}{filename_ext}'
        path = Path(S3_DOCUMENT_ROOT_DIRECTORY)
        if S3_PREFIX_QUERY_PARAM_NAME:
            prefix = request.GET.get(S3_PREFIX_QUERY_PARAM_NAME)
            if prefix:
                path /= prefix
        path /= _filename
        return str(path)

class S3Wrapper(object):
    _s3_client = None

    @classmethod
    def get_client(cls):
        if not cls._s3_client:
            logger.debug('Instantiating S3 client')
            extra_kwargs = {}
            if S3_ENDPOINT_URL:
                extra_kwargs['endpoint_url'] = S3_ENDPOINT_URL

            cls._s3_client = boto3.client(
                's3',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_REGION,
                **extra_kwargs)
        return cls._s3_client

def s3_client():
    return S3Wrapper.get_client()

class UploadFailed(Exception):
    pass

class ThreadedS3ChunkUploader(ThreadPoolExecutor):
    def __init__(self, client, bucket, key, upload_id, max_workers=None):
        max_workers = max_workers or 10
        self.bucket = bucket
        self.key = key
        self.upload_id = upload_id
        self.client = client
        self.part_number = 0
        self.parts = []
        self.queue = []
        self.current_queue_size = 0
        super().__init__(max_workers=max_workers)

    def add(self, body):
        if body:
            content_length = len(body)
            self.queue.append(body)
            self.current_queue_size += content_length

        if not body or self.current_queue_size > S3_MIN_PART_SIZE:
            self.part_number += 1
            _body = self.drain_queue()
            future = self.submit(
                self.client.upload_part,
                Bucket=self.bucket,
                Key=self.key,
                PartNumber=self.part_number,
                UploadId=self.upload_id,
                Body=_body,
                ContentLength=len(_body),
            )
            self.parts.append((self.part_number, future))
            logger.debug('Prepared part %s', self.part_number)

    def drain_queue(self):
        body = b''.join(self.queue)
        self.queue = []
        self.current_queue_size = 0
        return body

    def get_parts(self):
        return [{
            'PartNumber': part[0],
            'ETag': part[1].result()['ETag'],
            } for part in self.parts
        ]

class S3FileUploadHandler(FileUploadHandler):
    def new_file(self, *args, **kwargs):
        if MAX_UPLOAD_SIZE and self.content_length:
            if self.content_length > MAX_UPLOAD_SIZE:
                raise UploadFailed('File too large')

        super().new_file(*args, **kwargs)
        self.parts = []
        self.bucket_name = AWS_STORAGE_BUCKET_NAME
        file_name = self.file_name
        if CLEAN_FILE_NAME:
            file_name = slugify(self.file_name)
        self.s3_key = generate_object_key(self.request, file_name)
        self.client = s3_client()
        self.multipart = self.client.create_multipart_upload(
            Bucket=self.bucket_name,
            Key=self.s3_key,
            ContentType=self.content_type,
        )
        self.upload_id = self.multipart['UploadId']
        self.executor = ThreadedS3ChunkUploader(
            self.client,
            self.bucket_name,
            key=self.s3_key,
            upload_id=self.upload_id
        )

        # Import S3Boto3StorageFile and S3Boto3Storage here to avoid circular import
        from storages.backends.s3boto3 import S3Boto3StorageFile, S3Boto3Storage

        # Prepare a storages object as a file placeholder
        self.storage = S3Boto3Storage()
        self.file = S3Boto3StorageFile(self.s3_key, 'w', self.storage, self.content_type)

    def receive_data_chunk(self, raw_data, start):
        try:
            self.executor.add(raw_data)
        except Exception as exc:
            logger.exception('Upload Failed')
            self.abort_multipart()
            raise UploadFailed from exc

    def file_complete(self, file_size):
        """All data is received, so we have to complete the multipart upload.
        Return a Django File object that can be used as the uploaded file.
        """
        try:
            self.executor.add(None)
            parts = self.executor.get_parts()
            self.client.complete_multipart_upload(
                Bucket=self.bucket_name,
                Key=self.s3_key,
                UploadId=self.upload_id,
                MultipartUpload={'Parts': parts},
            )
            logger.debug('Upload complete')
            
            # Instead of setting the size directly, you can handle it differently if needed
            # Example: Just return the file object without setting size
            return self.file
        except Exception as exc:
            logger.error("Upload failed", exc_info=True)
            self.client.abort_multipart_upload(
                Bucket=self.bucket_name,
                Key=self.s3_key,
                UploadId=self.upload_id
            )
            raise UploadFailed from exc

    def abort_multipart(self):
        if hasattr(self, 'executor'):
            self.executor.shutdown()
        if hasattr(self, 'client'):
            try:
                self.client.abort_multipart_upload(
                    Bucket=self.bucket_name,
                    Key=self.s3_key,
                    UploadId=self.upload_id
                )
            except Exception:
                pass
