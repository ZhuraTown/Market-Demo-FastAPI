import sys
from loguru import logger

from src.config import settings
from src.utils.request_id import request_id_ctx


def add_request_id(record):
    record["extra"]["request_id"] = request_id_ctx.get() or "-"
    return record


def setup_logging():
    logger.remove()
    logger.add(
        sys.stdout,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "RID={extra[request_id]} | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "{message}"
        ),
        level="DEBUG" if settings.debug else "INFO",
        filter=add_request_id
    )