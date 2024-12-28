"""
Download file from S3 with meta data
"""
import requests
from constants.constants import ERROR_DOWNLOADING_FILE, MESSAGE_DOWNLOAD_SUCCESS

def download_file(presigned_url):
    """Download a file from an S3 bucket"""
    try: 
        response = requests.get(presigned_url)
        response.raise_for_status()

        if response.status_code == 200:
            print("Downloading image...")
            with open("downloaded_image.jpg", "wb") as f:
                return f.write(response.content)
    except:
        raise Exception(ERROR_DOWNLOADING_FILE)