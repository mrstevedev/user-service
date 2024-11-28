from functools import wraps
from flask_jwt_extended import get_jwt_identity
from models.User import UserModel
from constants.constants import ERROR_NOT_AUTHORIZED, ADMINISTRATOR

def admin_user():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            if UserModel.query.filter_by(role=ADMINISTRATOR, email=user_id).first() is None:
                raise Exception(ERROR_NOT_AUTHORIZED)
            return func(*args, **kwargs)
        return wrapper
    return decorator