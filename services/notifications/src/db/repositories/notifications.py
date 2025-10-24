from datetime import datetime, timezone
from typing import TypeVar

from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import WebSocketNotification, EmailNotification

NotificationType = TypeVar('NotificationType', EmailNotification, WebSocketNotification)


class NotificationsRepository:
    @classmethod
    async def create(cls, session: AsyncSession, data: EmailNotification) -> EmailNotification:
        session.add(data)
        await session.flush()
        return data

    @classmethod
    async def get_list(
            cls,
            session: AsyncSession,
            user_id: int,
            page: int = 1,
            per_page: int = 100,
    ) -> list[WebSocketNotification]:
        offset = (page - 1) * per_page
        res = await session.scalars(
            select(WebSocketNotification)
            .where(WebSocketNotification.user_id == user_id)
            .order_by(WebSocketNotification.id)
            .offset(offset)
            .limit(per_page)
        )
        return list(res)

    @classmethod
    async def mark_as_read(
            cls,
            session: AsyncSession,
            user_id: int,
            notification_ids: list[int]
    ) -> list[WebSocketNotification]:
        stmt = (
            update(WebSocketNotification)
            .where(
                WebSocketNotification.user_id == user_id,
                WebSocketNotification.id.in_(notification_ids)
            )
            .values(is_read=True)
            .returning(WebSocketNotification)
        )
        await session.flush()
        # todo: check it, how work
        return list(await session.scalars(stmt))

    @classmethod
    async def mark_as_read_all(
            cls,
            session: AsyncSession,
            user_id: int,
    ) -> None:
        stmt = (
            update(WebSocketNotification)
            .where(
                WebSocketNotification.user_id == user_id,
            )
            .values(is_read=True)
        )
        await session.execute(stmt)
        await session.flush()


    @classmethod
    async def count(
            cls,
            session: AsyncSession,
            user_id: int,
            as_read: bool | None = None,
    ) -> int:
        query = (
            select(func.count(WebSocketNotification.id))
            .where(WebSocketNotification.user_id == user_id,)
        )
        if as_read is not None:
            query = query.where(WebSocketNotification.is_read == as_read)
        res = await session.execute(query)
        return res.scalar_one()