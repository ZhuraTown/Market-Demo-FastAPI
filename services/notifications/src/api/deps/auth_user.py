from typing import Annotated

from fastapi import Depends

from src.db.models import User
from src.security.custom_auth import custom_authentication


def auth_user(
        user: Annotated[User, Depends(custom_authentication)],
) -> User:
    return user