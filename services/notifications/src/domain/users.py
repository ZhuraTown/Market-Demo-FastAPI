from sqlalchemy.ext.asyncio import AsyncSession

from src.consumers.dto import UserEventV1, EventType
from loguru import logger

from src.db.models import User, Notification


class UserService:

    @classmethod
    async def _process_create_user(
            cls,
            session: AsyncSession,
            event: UserEventV1,
    ):
        logger.info(f"Create new user: {event.data}")
        session.add(
            User(id=event.data.user_id, email=event.data.email)
        )
        session.add(
            Notification(
                user_id=event.data.user_id,
                title='Welcome Bro!',
                body={"message": "We are glad to see you with us."},
            )
        )

    @classmethod
    async def catch_event(cls,session: AsyncSession, event: UserEventV1):
        logger.info(f"UserService catch event: {event}")

        if event.type == EventType.CREATED:
            logger.info(f"Create new user: {event.data}")
            await cls._process_create_user(session, event)
        elif event.type == EventType.UPDATED:
            ...
        elif event.type == EventType.DELETED:
            ...
        await session.commit()
