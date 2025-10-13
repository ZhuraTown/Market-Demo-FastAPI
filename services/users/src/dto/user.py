from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    username: str
    email: EmailStr

class CreateUser(BaseUser):
    password: str


class ReadUser(BaseUser):
    id: int

class UpdateUser(BaseUser):
    ...