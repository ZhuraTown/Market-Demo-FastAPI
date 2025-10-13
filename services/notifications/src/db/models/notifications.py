from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base, DatetimeMixin


if TYPE_CHECKING:
    from src.db.models import User




class Notification(Base, DatetimeMixin):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped['User'] = relationship(
        "User", back_populates="notifications", foreign_keys=[user_id]
    )

    title: Mapped[str]
    body: Mapped[dict] = mapped_column(JSONB)

