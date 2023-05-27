from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import false, func, true

from server.database import Base

if TYPE_CHECKING:
    from server.monitored_users.models import MonitoredUser
    from server.social_auths.models import SocialAuth


class User(Base):
    __tablename__ = "users"

    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    receive_email: Mapped[bool] = mapped_column(server_default=true())
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    social_auths: Mapped[List["SocialAuth"]] = relationship(
        "SocialAuth", back_populates="user", cascade="all, delete-orphan"
    )
    monitored_users: Mapped[List["MonitoredUser"]] = relationship(
        "MonitoredUser", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r})"

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "email": self.email,
            "receive_email": self.receive_email,
        }
