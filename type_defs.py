import strawberry

@strawberry.type
class User:
    first_name: str
    last_name: str
    username: str
    email: str
    password: str

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