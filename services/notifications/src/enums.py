from enum import Enum


class EventType(str, Enum):
    CREATED = "CREATED"
    UPDATED = "UPDATED"
    DELETED = "DELETED"
    RECOVERED = "RECOVERED"
    RESET_PASSWORD = "RESET_PASSWORD"


class WSNotificationAction(str, Enum):
    MARK_AS_READ = "MARK_AS_READ"
    MARK_ALL_READ = "MARK_ALL_READ"
    PAGINATE = "PAGINATE"
