import asyncio
from logging.config import fileConfig

from sqlalchemy import engine_from_config, URL
from sqlalchemy import pool

from alembic import context

from app.config import settings
from app.db.create_database import create_database
from app.db.models import *  # noqa
from app.db.models.base import Base

asyncio.run(create_database())

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

url_connect = URL.create(
    drivername="postgresql+asyncpg",
    username=settings.db.user,
    password=settings.db.password,
    host=settings.db.host,
    port=settings.db.port,
    database=settings.db.name,
)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=url_connect,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configurations = config.get_section(config.config_ini_section, {})
    configurations["sqlalchemy.url"] = url_connect
    connectable = engine_from_config(
        configurations,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
