

This project is a Desktop Agent Application that monitors user activities, captures screenshots periodically, tracks mouse and keyboard activities, and handles internet connection and battery status warnings. The application is built using Python with a Tkinter-based UI and integrates with AWS S3 for storing captured screenshots.

## Features

- **Full-Screen Mode**: The application runs in full-screen mode, similar to secure exam launchers.
- **Activity Tracking**: Monitors mouse and keyboard activity.
- **Screenshot Capture**: Captures screenshots at regular intervals with optional blurring.
- **Timezone Detection**: Detects and logs timezone changes.
- **Internet & Battery Monitoring**: Warns the user when the internet connection is low or when the battery is low.
- **AWS S3 Integration**: Uploads captured screenshots to an AWS S3 bucket.

## Installation

### Prerequisites

Ensure that you have the following installed:

- Python 3.9 or later
- Pip (Python package installer)
- AWS CLI configured with appropriate credentials

## Output

![Screenshot 2024-08-26 140809](https://github.com/user-attachments/assets/04bc3614-b5e4-4617-b5e3-c1b516bc100a)

![aws-storage](https://github.com/user-attachments/assets/def5269d-f429-4620-bb53-ac6288103c5b)
![Screenshot 2024-08-26 140354](https://github.com/user-attachments/assets/bacfa587-99c1-44df-af26-e3744943bd81)
![Screenshot 2024-08-26 140635](https://github.com/user-attachments/assets/0ad4c748-d80c-4dca-863f-e61a54e9ce9b)


### Clone the Repository

```bash
git clone https://github.com/Markandey2002/Desktop_Agent.git
cd Desktop_Agent


