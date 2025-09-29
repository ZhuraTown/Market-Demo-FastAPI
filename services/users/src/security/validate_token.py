from jose import jwt
from loguru import logger

from src.config import settings


def verify_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            token,
            settings.security.public_secret_key,
            algorithms=[settings.security.algorithm],
        )
        return payload
    except Exception as e:
        logger.error(
            f"decode_jwt_token: Failed to decode JWT - {type(e).__name__}: {e}"
        )
        return None
