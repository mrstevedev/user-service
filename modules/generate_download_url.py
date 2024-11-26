
import boto3
from botocore.config import Config
from constants.constants import AWS_SERVICE, ERROR_OBJECT_NOT_EXISTS

"""
Generate Presigned Download URL
"""
def generate_presigned_download_url(bucket_name, object_name, expiration=3600) -> str:
    """Generate a presigned URL for downloading a file from S3"""

    s3 = boto3.resource(AWS_SERVICE)
    s3_client = boto3.client(AWS_SERVICE, config=Config(signature_version='s3v4'))

    try:
        s3.Object(bucket_name, object_name).load()

        response = s3_client.generate_presigned_url('get_object', Params={
        'Bucket': bucket_name,
        'Key': object_name }, ExpiresIn=expiration
        )

        return response
    except:
        raise Exception(ERROR_OBJECT_NOT_EXISTS)