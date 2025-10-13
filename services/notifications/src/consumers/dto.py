from datetime import datetime

from pydantic import BaseModel, Field
from enum import Enum


class EventType(str, Enum):
    CREATED = "CREATED"
    UPDATED = "UPDATED"
    DELETED = "DELETED"
    RESET_PASSWORD = "RESET_PASSWORD"

class MetaData(BaseModel):
    event_id: str
    event_timestamp: datetime = Field(default_factory=datetime.utcnow)

class UserData(BaseModel):
    user_id: int
    email: str

class UserEventV1(BaseModel):
    metadata: MetaData
    type: EventType
    data: UserData