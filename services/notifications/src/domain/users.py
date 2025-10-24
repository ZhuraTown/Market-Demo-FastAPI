from typing import Callable

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.consumers.dto import UserEventV1
from src.enums import EventType
from loguru import logger

from src.db.models import User, WebSocketNotification
from src.domain.emails import EmailSenderService
from src.dto.email import EmailWelcomeDTO, EmailResetPasswordDTO


class UserEventProcessor:

    def __init__(
            self,
            session: AsyncSession,
            email_service: EmailSenderService,
    ):
        self.session = session
        self.email_service = email_service

    async def _process_create_user(
            self,
            event: UserEventV1,
    ):
        logger.info(f"Create new user: {event.data}")
        self.session.add(
            User(id=event.data.user_id, email=event.data.email)
        )
        # todo: add logic for send notification to WS
        # self.session.add(
        #     WebSocketNotification(
        #         user_id=event.data.user_id,
        #         title='Welcome Bro!',
        #         body={"message": "We are glad to see you with us."},
        #     )
        # )
        await self.email_service.send_email_welcome(
            data=EmailWelcomeDTO(email=event.data.email, user_id=event.data.user_id)
        )

    async def _process_update_user(self, event: UserEventV1):
        logger.info(f"Update user: {event.data}")
        await self.session.execute(
            update(User)
            .where(User.id == event.data.user_id)
            .values(email=event.data.email)
        )

    async def _process_delete_user(self, event: UserEventV1):
        logger.info(f"Delete user: {event.data}")
        await self.session.execute(
            update(User)
            .where(User.id == event.data.user_id)
            .values(deleted_at=event.metadata.event_timestamp)
        )

    async def _process_recover_user(self, event: UserEventV1):
        logger.info(f"Recover user: {event.data}")
        await self.session.execute(
            update(User)
            .where(User.id == event.data.user_id)
            .values(deleted_at=None)
        )

    async def _process_reset_password_user(self, event: UserEventV1):
        logger.info(f"Reset password user: {event.data}")
        reset_password_url = event.data.reset_url
        await self.email_service.send_email_reset_password(
            data=EmailResetPasswordDTO(user_id=event.data.user_id, reset_password_url=reset_password_url)
        )

    async def process_event(self, event: UserEventV1):
        logger.info(f"UserService catch event: {event}")
        handlers: dict[EventType, Callable] = {
            EventType.CREATED: self._process_create_user,
            EventType.UPDATED: self._process_update_user,
            EventType.DELETED: self._process_delete_user,
            EventType.RECOVERED: self._process_recover_user,
            EventType.RESET_PASSWORD: self._process_reset_password_user,
        }
        handler = handlers.get(event.type)
        if not handler:
            logger.error(f"No handler for event type: {event.type}")
            return

        await handler(event)
        await self.session.commit()
