import os

host = os.environ.get("POSTGRES_HOST")
username = os.environ.get("POSTGRES_USERNAME")
password = os.environ.get("POSTGRES_PASSWORD")
database = os.environ.get("POSTGRES_DB")
port = os.environ.get("POSTGRES_PORT")

USER = "User"
ADMINISTRATOR = "Administrator"
ADMIN_EMAIL = "leanne@gmail.com"
ERROR_USER_EXISTS = "User with this email already exists"
ERROR_USER_NOT_EXISTS = "User does not exists"
ERROR_INVALID_PASSWORD = "Invalid password"
SQLALCHEMY_DATABASE_URL = f'postgresql://{username}:{password}@{host}:{port}/{database}'
SUPER_SECRET_KEY = "20149e340d630235109558b3548af106d928fcefcb85f665440fb12f9fa716c0909d6b2025857ef690e73cf4330a5076a22ef7b6291e15357d4e5358090610e1"
ERROR_NOT_AUTHORIZED="You are not authorized to perform this action"
MAX_TOKEN_DAYS = 30
MAX_TOKEN_SECONDS = 15
AWS_SERVICE = "s3"
ERROR_GENERATING_UPLOAD_URL = "Error generating presigned upload URL"
ERROR_GENERATING_DOWNLOAD_URL = "Error generating presigned upload URL"
ERROR_OBJECT_NOT_EXISTS = "Object does not exist"
ERROR_UPLOADING_FILE = "Error uploading file to S3"
ERROR_DOWNLOADING_FILE = "Error downloading file from S3"
ERROR_NO_URL_AND_FILE_PATH = "No URL and file path provided"
ERROR_NO_PRESIGNED_DOWNLOAD_URL = "No presigned download URL provided"
MESSAGE_UPLOAD_SUCCESS = "File uploaded successfully"
MESSAGE_DOWNLOAD_SUCCESS = "File downloaded successfully"