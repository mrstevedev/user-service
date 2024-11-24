import strawberry
from datetime import timedelta
from modules.hash import hashPassword
from modules.decode import decodePassword
from modules.logger import logger
from models.models import UserModel, db
from queries import User
from constants.constants import ERROR_USER_EXISTS, ERROR_USER_NOT_EXISTS, ERROR_INVALID_PASSWORD
from modules.create import access_token
from modules.refresh import refresh
from flask_jwt_extended import jwt_required
from type_defs import UpdateUserInput, UserLoginInput, User, UserSignin, Event
from decorators.admin_user import admin_user

@strawberry.type
class Mutation: 
    """
    User Registration
    """
    @strawberry.mutation
    def register_user(self, first_name: str, last_name: str, username: str, email: str, password: str) -> User:
        logger.info("Creating user with first_name: %s, last_name: %s, username: %s, email: %s, password: %s", first_name, last_name, username, email, password)
        user = UserModel(first_name=first_name, last_name=last_name, username=username, email=email, password=hashPassword(password))
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
        
        refresh_token = refresh(user.email, refresh_payload, timedelta(days=30))
    
        response = UserSignin(access_token=access_token(user.email, access_payload, timedelta(minutes=15)))

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
    Update User
    """
    @strawberry.mutation
    def update_user(self, input: UpdateUserInput) -> User:
        logger.info("updating user with id: %s", input.id)
        user = UserModel.query.get(input.id)

        if not user or user.id != input.id:
            raise Exception(ERROR_USER_NOT_EXISTS)
        
        user.first_name = input.first_name
        user.last_name = input.last_name
        user.username = input.username
        user.password = hashPassword(input.password)
        user.email = input.email
        db.session.commit()
        
        return user
