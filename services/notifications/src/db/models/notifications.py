from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base, DatetimeMixin


if TYPE_CHECKING:
    from src.db.models import User




class WebSocketNotification(Base, DatetimeMixin):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped['User'] = relationship(
        "User", back_populates="ws_notifications", foreign_keys=[user_id]
    )

    title: Mapped[str]
    body: Mapped[dict] = mapped_column(JSONB)

    is_read: Mapped[bool] = mapped_column(default=False)
    source: Mapped[str] = mapped_column(index=True)

    def __repr__(self) -> str:
        return f"WebSocketNotification(id={self.id}, user_id={self.user_id}, title={self.title}, source={self.source})"

class EmailNotification(Base, DatetimeMixin):
    __tablename__ = "email_notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped['User'] = relationship(
        "User", back_populates="email_notifications", foreign_keys=[user_id]
    )

    recipient_email: Mapped[str]
    header: Mapped[str]
    subject: Mapped[str]
    source: Mapped[str] = mapped_column(index=True)

    template_params: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    error_message: Mapped[str | None] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"EmailNotification(id={self.id}, user_id={self.user_id}, email={self.recipient_email}, header={self.header})"