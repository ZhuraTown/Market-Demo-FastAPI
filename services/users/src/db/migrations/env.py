import asyncio
from logging.config import fileConfig

from sqlalchemy import URL
from sqlalchemy import pool

from alembic import context
from sqlalchemy.engine.base import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from src.config import settings
from src.db.create_database import create_database
from src.db.models import *  # noqa
from src.db.models.base import Base

asyncio.run(create_database())

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

url_connect = URL.create(
    drivername="postgresql+asyncpg",
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=url_connect,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    configurations = config.get_section(config.config_ini_section, {})
    configurations["sqlalchemy.url"] = url_connect
    connectable = async_engine_from_config(
        configurations,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

