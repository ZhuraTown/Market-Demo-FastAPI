from datetime import datetime, UTC, timedelta

from jose import jwt

from src.config import settings


def create_token(data: dict, ttl: int) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(seconds=ttl)
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.sec_private_secret_key,
        algorithm=settings.sec_algorithm,
    )
