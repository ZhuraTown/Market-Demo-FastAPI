from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class Base(AsyncAttrs, DeclarativeBase):
    type_annotation_map = {
        dict[str, Any]: JSONB,
        dict: JSONB,
    }


class DatetimeMixin(DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=True,
        index=True,
    )
    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
