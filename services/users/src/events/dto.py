from datetime import datetime

from pydantic import BaseModel, Field
from enum import Enum


class EventType(str, Enum):
    CREATED = "CREATED"
    UPDATED = "UPDATED"
    DELETED = "DELETED"
    RECOVERED = "RECOVERED"
    RESET_PASSWORD = "RESET_PASSWORD"

class MetaData(BaseModel):
    event_id: str
    event_timestamp: datetime = Field(default_factory=datetime.utcnow)

class UserData(BaseModel):
    user_id: int = Field(..., validation_alias="id")
    email: str

class UserResetPasswordData(BaseModel):
    user_id: int
    reset_url: str

class UserEventV1(BaseModel):
    metadata: MetaData
    type: EventType
    data: UserData | UserResetPasswordData