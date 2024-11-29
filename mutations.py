import os
import strawberry
from datetime import timedelta
from modules.hash import hashPassword
from modules.decode import decodePassword
from modules.logger import logger
from models.models import UserModel, db
from constants.constants import (
     ADMINISTRATOR,
     MAX_TOKEN_SECONDS,
     ERROR_USER_EXISTS, 
     USER, MAX_TOKEN_DAYS, 
     ERROR_UPLOADING_FILE,
     ERROR_USER_NOT_EXISTS, 
     ERROR_INVALID_PASSWORD,
     ERROR_NO_URL_AND_FILE_PATH,
     ERROR_GENERATING_UPLOAD_URL,
     ERROR_GENERATING_DOWNLOAD_URL,
     MESSAGE_UPLOAD_SUCCESS,
)
from modules.refresh import refresh
from modules.upload import upload_file
from modules.create import access_token
from modules.generate_upload_url import generate_presigned_upload_url
from modules.generate_download_url import generate_presigned_download_url

from flask_jwt_extended import jwt_required
from type_defs import (
    UpdateUserInput, UserLoginInput, UserSignin, Event, AWSS3Input, AWSS3UploadInput, 
    DeleteSuccess, UpdateSuccess, RegisterSuccess, UploadSuccess)
from decorators.admin_user import admin_user

@strawberry.type
class Mutation: 
    """
    User Registration
    """
    @strawberry.mutation
    def register_user(self, first_name: str, last_name: str, username: str, email: str, password: str) -> User:
        logger.info("Creating user with first_name: %s, last_name: %s, username: %s, email: %s, password: %s", first_name, last_name, username, email, password)
        user = UserModel(first_name=first_name, last_name=last_name, username=username, email=email, password=hashPassword(password), role=USER)
        check_user = UserModel.query.filter_by(email=email).first()
        
        if check_user:
            raise Exception(ERROR_USER_EXISTS)
        
        db.session.add(user)
        db.session.commit()
        
        return user
    
    """
    User Login
    """
    @strawberry.mutation
    def login_user(self, input: UserLoginInput, info: strawberry.Info) -> UserSignin:
        logger.info("Signing in user with email: %s", input.email)
        user = UserModel.query.filter_by(email=input.email).first()

        if not user:
            raise Exception(ERROR_USER_NOT_EXISTS)

        if not decodePassword(user.password, input.password):
            raise Exception(ERROR_INVALID_PASSWORD)
        
        access_payload = {"email": user.email,"password": user.password}
        refresh_payload = {"email": user.email,"password": user.password}
        
        refresh_token = refresh(user.email, refresh_payload, timedelta(days=MAX_TOKEN_DAYS))
    
        response = UserSignin(access_token=access_token(user.email, access_payload, timedelta(minutes=MAX_TOKEN_SECONDS)))

        info.context["response"].set_cookie(
            key="refresh_token", 
            value=refresh_token,
            httponly=True
        )
        
        return response

    """
    Delete User
    """        
    @strawberry.mutation
    def delete_user(self, id: int) -> User:
        logger.info("Deleting user with id: %s", id)
        user = UserModel.query.get(id)

        if not user or user.id != id:
            raise Exception(ERROR_USER_NOT_EXISTS)
        
        db.session.delete(user)
        db.session.commit()
        
        return user

    """
    Create Event
    """
    @strawberry.mutation
    @jwt_required()
    def create_event(self, title: str, description: str, start_time: str, end_time: str, venue: str) -> Event:
        logger.info(
            "Creating event with title: %s, description: %s, start_time: %s, end_time: %s, venue: %s", 
            title, description, start_time, end_time, venue)
        
    """
    Admin Update
    """
    @strawberry.mutation
    @jwt_required()
    @admin_user()
    def admin_update_user(self, input: UpdateUserInput) -> User:
        logger.info("Admin updating user with id: %s", input.id)
        user = UserModel.query.get(input.id)

        if not user or user.id != input.id:
            raise Exception(ERROR_USER_NOT_EXISTS)
        
        user.first_name = input.first_name
        user.last_name = input.last_name
        user.username = input.username
        user.password = hashPassword(input.password)
        user.email = input.email
        user.role = input.role
        db.session.commit()
        
        return user
    
    """
    Generate presigned upload URL
    """
    @strawberry.mutation
    @jwt_required()
    def generate_presigned_s3_upload_url(self, input: AWSS3Input) -> str:
        logger.info("Generating presigned upload URL")
       
        response = generate_presigned_upload_url(
            os.environ.get("AWS_S3_BUCKET_NAME"), input.key)
        
        if not response:
            raise Exception(ERROR_GENERATING_UPLOAD_URL)

        return response
    
    """
    Generate presigned download URL
    """
    @strawberry.mutation
    @jwt_required()
    def generate_presigned_s3_download_url(self, input: AWSS3Input) -> str:
        logger.info("Generating presigned download URL")

        response = generate_presigned_download_url(
            os.environ.get("AWS_S3_BUCKET_NAME"), input.key)
        
        if not response:
            raise Exception(ERROR_GENERATING_DOWNLOAD_URL)

        return response
    
    """
    Upload file using presigned upload URL
    """
    @strawberry.mutation
    @jwt_required()
    def upload_file(self, input: AWSS3UploadInput) -> str:
        logger.info("Uploading file to S3")

        if not input.presigned_url and not input.file_path:
            raise Exception(ERROR_NO_URL_AND_FILE_PATH)
        
        try: 
            upload_file(input.presigned_url, input.file_path)
            
            return MESSAGE_UPLOAD_SUCCESS
        except:
            raise Exception(ERROR_UPLOADING_FILE)
