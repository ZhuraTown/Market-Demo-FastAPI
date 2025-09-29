import asyncpg
import logging
import sys
from loguru import logger
from app.config import settings


async def create_database():
    try:
        if not settings.db.create:
            logger.warning("Dont create database")
            return
        connection = await asyncpg.connect(
            user=settings.db.user,
            password=settings.db.password,
            host=settings.db.host,
            port=settings.db.port,
            database="postgres",
        )
        db_is_exist = await connection.fetchval(
            f"SELECT 1 FROM pg_database WHERE datname='{settings.db.name}'",
        )
        if not db_is_exist:
            logging.warning(f"CREATE DATABASE {settings.db.name}")
            await connection.execute(
                f"CREATE DATABASE {settings.db.name};"
            )
        await connection.close()
    except Exception as e:
        logger.critical(f"Create database {settings.db.name} failed: {e}")
        sys.exit(1)
