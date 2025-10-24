import math
from loguru import logger
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket

from src.api.ws.manager import NotificationConnectionManager
from src.db.database import db
from src.db.repositories.notifications import NotificationsRepository
from src.dto.notification import NotificationItemDTO, NotificationPaginatedDTO, PaginationMeta, NotificationActionInput, \
    NotificationPaginate
from src.enums import WSNotificationAction


class NotificationService:

    @classmethod
    async def get_paginated_notifications(
            cls,
            session: AsyncSession,
            user_id: int,
            page: int,
            per_page: int,
    ) -> NotificationPaginatedDTO:
        logger.info(f"Getting notifications for user {user_id}")
        notifications = await NotificationsRepository.get_list(session, user_id, page, per_page)
        total = await NotificationsRepository.count(session, user_id)
        count_as_read = await NotificationsRepository.count(session, user_id, as_read=False)
        pages = math.ceil(total / per_page)
        return NotificationPaginatedDTO(
            items=[NotificationItemDTO.model_validate(n, from_attributes=True) for n in notifications],
            meta=PaginationMeta(
                page=page,
                pages=pages,
                per_page=per_page,
                total=total,
                count_as_read=count_as_read,
                next_page=page + 1 if page < pages else None,
                prev_page=page - 1 if page > 1 else None,
            )
        )
    @classmethod
    async def mark_as_read_all(
            cls,
            session: AsyncSession,
            user_id: int,
    ):
        logger.info(f"Mark notifications as read all for user({user_id})")
        await NotificationsRepository.mark_as_read_all(session, user_id)
        await session.commit()




class NotificationActionHandler:

    @classmethod
    async def handle(
            cls,
            user_id: int,
            websocket: WebSocket,
            manager: NotificationConnectionManager,
            data: dict
    ):
        try:
            validated = NotificationActionInput.model_validate(data, from_attributes=True)
        except ValidationError as e:
            await manager.send_personal_message(
                {"status": "error", "message": "Invalid payload", "errors": e.errors()},
                websocket
            )
            return

        async with db.session() as session:
            match validated.action:
                case WSNotificationAction.PAGINATE:
                    await cls._handle_paginate(user_id,session, websocket, manager, validated.params)
                # case WSNotificationActions.MARK_AS_READ:
                #     await self._handle_mark_as_read(service, user_id, websocket, validated.params)
                case WSNotificationAction.MARK_ALL_READ:
                    await cls._handle_mark_all_read(user_id, session, websocket, manager)
                case _:
                    await manager.send_personal_message(
                        {"status": "error", "message": f"Unknown action {validated.action}"}, websocket
                    )

    @classmethod
    async def _handle_paginate(
            cls,
            user_id,
            session: AsyncSession,
            websocket: WebSocket,
            manager: NotificationConnectionManager,
            data: NotificationPaginate
    ):
        notifications = await NotificationService.get_paginated_notifications(
            session, user_id, data.page, data.per_page
        )
        await manager.send_personal_message(
            notifications.model_dump(mode='json'), websocket
        )

    async def _handle_mark_as_read(self, service, user_id, websocket, params):
        await service.mark_as_read(user_id, params.notification_id)
        await self.manager.send_personal_message(
            {"status": "ok", "message": "Notification marked as read"}, websocket
        )

    @classmethod
    async def _handle_mark_all_read(
            cls,
            user_id,
            session: AsyncSession,
            websocket: WebSocket,
            manager: NotificationConnectionManager,
    ):
        await NotificationService.mark_as_read_all(session, user_id)
        await manager.send_personal_message(
            {"status": "ok", "message": "Success"}, websocket
        )