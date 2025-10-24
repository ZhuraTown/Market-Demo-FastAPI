from pydantic import BaseModel, model_validator

from src.enums import WSNotificationAction


class NotificationPaginate(BaseModel):
    page: int
    per_page: int

class NotificationMarkAsRead(BaseModel):
    notification_ids: list[int]


class NotificationActionInput(BaseModel):
    action: WSNotificationAction
    params: NotificationPaginate | NotificationMarkAsRead | None = None

    @model_validator(mode='after')
    def validate(self):
        if self.action == WSNotificationAction.PAGINATE and not isinstance(self.params, NotificationPaginate):
            raise ValueError(f'Action Paginate must have params: {NotificationPaginate.model_fields}')
        return self


class NotificationItemDTO(BaseModel):
    id: int
    title: str
    body: dict
    is_read: bool
    source: str

class PaginationMeta(BaseModel):
    page: int
    pages: int
    per_page: int
    total: int
    count_as_read: int
    next_page: int | None
    prev_page: int | None

class NotificationPaginatedDTO(BaseModel):
    meta: PaginationMeta
    items: list[NotificationItemDTO]
