from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.base import Base, DatetimeMixin


class User(Base, DatetimeMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    # roles
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_seller: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"<User username:{self.username}, is_admin: {self.is_admin}, is_seller: {self.is_seller}>"

