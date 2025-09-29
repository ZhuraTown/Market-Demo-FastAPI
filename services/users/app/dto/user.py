from pydantic import BaseModel


class BaseUserDTO(BaseModel):
    username: str
    email: str

class CreateUserDTO(BaseUserDTO):
    password: str


class UserInfoDTO(BaseUserDTO):
    id: int
    ...
