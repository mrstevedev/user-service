"""
Upload file to S3 with meta data
"""
import requests
from constants.constants import ERROR_UPLOADING_FILE, MESSAGE_UPLOAD_SUCCESS

def upload_file(presigned_url, file_path):
    """Upload a file to an S3 bucket"""
    try: 

        headers = { "Content-Type": "image/jpeg" }

        response = requests.put(presigned_url, data=open(file_path, "rb"), headers=headers)
        response.raise_for_status()

        return MESSAGE_UPLOAD_SUCCESS
    except:
        raise Exception(ERROR_UPLOADING_FILE)