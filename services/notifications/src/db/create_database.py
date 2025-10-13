import asyncpg
import logging
import sys
from loguru import logger
from src.config import settings


async def create_database():
    try:
        if not settings.db_create:
            logger.warning("Dont create database")
            return
        connection = await asyncpg.connect(
            user=settings.db_user,
            password=settings.db_password,
            host=settings.db_host,
            port=settings.db_port,
            database="postgres",
        )
        db_is_exist = await connection.fetchval(
            f"SELECT 1 FROM pg_database WHERE datname='{settings.db_name}'",
        )
        if not db_is_exist:
            logging.warning(f"CREATE DATABASE {settings.db_name}")
            await connection.execute(f"CREATE DATABASE {settings.db_name};")
        await connection.close()
    except Exception as e:
        logger.critical(f"Create database {settings.db_name} failed: {e}")
        sys.exit(1)
