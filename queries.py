import typing
import strawberry
from datetime import timedelta
from modules.logger import logger
from models.models import UserModel, db
from type_defs import User, Message
from flask_jwt_extended import jwt_required, get_jwt_identity
from modules.create import access_token

def users():
    logger.info("Getting users")
    return db.session.query(
        UserModel.id, UserModel.first_name, UserModel.last_name, UserModel.username, UserModel.email, UserModel.role).all()

def logout(info: strawberry.Info) -> Message:
    logger.info("Logging out user")
    info.context["response"].delete_cookie("refresh_token")
    return Message(message="Successfully logged out")

"""
Refresh resolver
"""
@jwt_required(refresh=True)
def refresh_token() -> str:
    logger.info("Refreshing token")
    identity = get_jwt_identity()
    password = UserModel.query.filter_by(email=identity).first().password
    refresh_payload = {"email": identity, "password": password}
    
    token = access_token(identity=identity, additional_claims=refresh_payload, expires_delta=timedelta(minutes=15))
    return token

@strawberry.type
class Query:
    users: typing.List[User] = strawberry.field(resolver=users)
    logout_user: Message = strawberry.field(resolver=logout)
    access_token: str = strawberry.field(resolver=refresh_token)
    