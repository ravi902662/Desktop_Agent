import time
from io import BytesIO
from datetime import datetime
from PIL import ImageGrab, ImageFilter
from django.http import HttpRequest
import os
from file_handler import S3FileUploadHandler  # Import your S3FileUploadHandler class

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenshot app.settings')
import django
django.setup()

def capture_screenshot(blur=False, delay=15):
    # Wait for the specified delay
    time.sleep(delay)

    # Capture the screenshot
    screenshot = ImageGrab.grab()
    
    # Apply blur if specified
    if blur:
        screenshot = screenshot.filter(ImageFilter.GaussianBlur(15))

    # Generate a unique filename with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"

    # Save the screenshot to an in-memory file
    in_memory_file = BytesIO()
    screenshot.save(in_memory_file, format="PNG")
    in_memory_file.seek(0)  # Go to the beginning of the file

    # Prepare a mock Django request to use with S3FileUploadHandler
    request = HttpRequest()
    request.method = 'POST'
    request.FILES = {}
    request.GET = {}  # You can add query parameters if needed

    # Create an instance of S3FileUploadHandler
    upload_handler = S3FileUploadHandler(request)
    upload_handler.new_file(
        file_name=filename,
        content_type='image/png',
        content_length=in_memory_file.getbuffer().nbytes,
        field_name='file'  # Add this argument
    )

    # Directly handle the chunk data
    upload_handler.receive_data_chunk(in_memory_file.read(), start=0)

    # Finish the upload
    uploaded_file = upload_handler.file_complete(file_size=in_memory_file.getbuffer().nbytes)

    # Cleanup
    in_memory_file.close()

    return uploaded_file