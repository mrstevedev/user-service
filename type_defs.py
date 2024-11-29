import strawberry
from constants.constants import USER

@strawberry.type
class User:
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    role: str = USER

@strawberry.input
class UpdateUserInput:
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    role: str

@strawberry.input
class UserLoginInput:
    email: str
    password: str

@strawberry.type
class Message:
    message: str

@strawberry.type
class UserSignin:
    access_token: str

@strawberry.type
class Event:
    title: str
    description: str
    start_time: str
    end_time: str
    venue: str

@strawberry.input
class AWSS3Input:
    key: str

@strawberry.input
class AWSS3UploadInput:
    presigned_url: str
    file_path: str

@strawberry.type
class DeleteSuccess:
    message: str

@strawberry.type
class UpdateSuccess:
    message: str

@strawberry.type
class RegisterSuccess:    
    message: str

@strawberry.type
class UploadSuccess:    
    message: str