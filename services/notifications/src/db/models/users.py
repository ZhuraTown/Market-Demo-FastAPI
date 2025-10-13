from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base, DatetimeMixin

if TYPE_CHECKING:
    from src.db.models import Notification

class User(Base, DatetimeMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)

    notifications: Mapped[list['Notification']] = relationship(
        "Notification", back_populates="user"
    )

    def __repr__(self):
        return f"<User username:{self.id}, email: {self.email}>"
