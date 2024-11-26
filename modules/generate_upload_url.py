
import os
import boto3
from botocore.config import Config
from constants.constants import AWS_SERVICE

"""
Generate Presigned Upload URL
"""
def generate_presigned_upload_url(bucket_name, object_name, expiration=3600) -> str:
    """Generate a presigned URL for uploading a file to S3"""

    s3_client = boto3.client(AWS_SERVICE, region_name=os.environ.get("AWS_REGION"), config=Config(signature_version='s3v4'))

    response = s3_client.generate_presigned_url('put_object', Params={
            'Bucket': bucket_name, 'Key': object_name }, ExpiresIn=expiration
    )

    return response