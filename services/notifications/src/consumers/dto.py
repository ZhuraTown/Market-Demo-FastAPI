from datetime import datetime

from pydantic import BaseModel, Field

from src.enums import EventType


class MetaData(BaseModel):
    event_id: str
    event_timestamp: datetime = Field(default_factory=datetime.utcnow)

class UserData(BaseModel):
    user_id: int
    email: str

class UserResetPasswordData(BaseModel):
    user_id: int
    reset_url: str

class UserEventV1(BaseModel):
    metadata: MetaData
    type: EventType
    data: UserData | UserResetPasswordData