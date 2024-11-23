import typing
import strawberry
from modules.logger import logger
from models.models import UserModel, db
from type_defs import User

def get_users():
    logger.info("Getting users")
    return db.session.query(UserModel).all()

@strawberry.type
class Query:
    users: typing.List[User] = strawberry.field(resolver=get_users)