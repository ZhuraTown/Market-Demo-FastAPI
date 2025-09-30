from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User


class UserRepository:
    @classmethod
    async def create(cls, session: AsyncSession, user: User) -> User:
        session.add(user)
        await session.flush()
        return user

    @classmethod
    async def get_by_id(cls, session: AsyncSession, pk: int) -> User | None:
        return await session.scalar(select(User).where(User.id == pk))

    @classmethod
    async def get_by_username(cls, session: AsyncSession, username: str) -> User | None:
        return await session.scalar(select(User).where(User.username == username))

    @classmethod
    async def get_by_email(cls, session: AsyncSession, email: str) -> User | None:
        return await session.scalar(select(User).where(User.email == email))

    @classmethod
    async def delete(cls, session: AsyncSession, pk: int) -> None:
        await session.execute(
            update(User)
            .where(User.id == pk)
            .values(deleted_at=datetime.now(timezone.utc))
        )
