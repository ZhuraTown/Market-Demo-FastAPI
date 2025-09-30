from pydantic import BaseModel


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