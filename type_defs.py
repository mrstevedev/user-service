    
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

@strawberry.input
class UserLoginInput:
    email: str
    password: str