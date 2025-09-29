from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]


    def __repr__(self):
        return f"<User {self.username}>"