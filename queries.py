import typing
import strawberry
from modules.logger import logger
from models.models import UserModel, db
from type_defs import User, Message

def users():
    logger.info("Getting users")
    return db.session.query(UserModel).all()

def logout(info: strawberry.Info) -> Message:
    logger.info("Logging out user")
    info.context["response"].delete_cookie("refresh_token")
    return Message(message="Successfully logged out")

@strawberry.type
class Query:
    users: typing.List[User] = strawberry.field(resolver=users)
    logout_user: Message = strawberry.field(resolver=logout)