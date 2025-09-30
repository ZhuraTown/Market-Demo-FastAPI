from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps.db import get_session
from src.db.models import User
from src.dto.auth import TokenData
from src.security.custom_auth import custom_authentication


def auth_user(
        user: Annotated[User, Depends(custom_authentication)],
) -> User:
    return user