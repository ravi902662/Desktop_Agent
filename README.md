This project is a Desktop Agent Application that monitors user activities, captures screenshots periodically, tracks mouse and keyboard activities, and handles internet connection and battery status warnings. The application is built using Python with a Tkinter-based UI and integrates with AWS S3 for storing captured screenshots.

Features
    Full-Screen Mode: The application runs in full-screen mode, similar to secure exam launchers.
    Activity Tracking: Monitors mouse and keyboard activity.
    Screenshot Capture: Captures screenshots at regular intervals with optional blurring.
    Timezone Detection: Detects and logs timezone changes.
    Internet & Battery Monitoring: Warns the user when the internet connection is low or when the battery is low.
    AWS S3 Integration: Uploads captured screenshots to an AWS S3 bucket.

Installation
Prerequisites
Ensure that you have the following installed:

Python 3.9 or later
Pip (Python package installer)
AWS CLI configured with appropriate credentials
