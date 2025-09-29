from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import db


async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    async with db.session() as session:
        yield session