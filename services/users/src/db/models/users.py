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


# todo: add later
# class Profile(Base):
#     __tablename__ = "profiles"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#
#     full_name: Mapped[str]
#     phone: Mapped[str | None] = mapped_column(nullable=True)
#     birth_date: Mapped[date] = mapped_column(nullable=True)
