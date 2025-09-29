from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import URL
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from src.config import settings


class Database:
    def __init__(self) -> None:
        self.engine = create_async_engine(
            URL.create(
                drivername="postgresql+asyncpg",
                username=settings.db_user,
                password=settings.db_password,
                host=settings.db_host,
                port=settings.db_port,
                database=settings.db_name,
            ),
            pool_recycle=1800,
            pool_pre_ping=True,
            pool_size=settings.db_pool_size,
            max_overflow=settings.db_max_overflow,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[type[AsyncSession], None]:
        async with self.session_factory() as session:
            try:
                yield session
            except DatabaseError as e:
                await session.rollback()
                raise
            finally:
                await session.close()


db = Database()
