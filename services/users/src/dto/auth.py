from pydantic import BaseModel, EmailStr


class CreateToken(BaseModel):
    username: str
    password: str

class ReadToken(BaseModel):
    access_token: str
    refresh_token: str

class RefreshToken(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    user_id: int


class ResetPassword(BaseModel):
    email: EmailStr

class ConfirmResetPassword(BaseModel):
    token: str
    password: str