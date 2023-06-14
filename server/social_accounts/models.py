from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from server.database import Base
from server.monitored_users.models import MonitoredUser

if TYPE_CHECKING:
    from server.posts.models import Post


class SocialAccount(Base):
    __tablename__ = "social_accounts"

    username: Mapped[str]
    url: Mapped[str]
    social_account_id: Mapped[str]
    profile_pic_url: Mapped[str] = mapped_column(nullable=True)
    type: Mapped[str]
    last_scanned: Mapped[datetime] = mapped_column(server_default=func.now())

    monitored_user_id: Mapped[UUID] = mapped_column(ForeignKey("monitored_users.id"))
    monitored_user: Mapped["MonitoredUser"] = relationship(
        "MonitoredUser", back_populates="social_accounts"
    )

    posts: Mapped[List["Post"]] = relationship(
        "Post", back_populates="social_account", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"MonitoredUser(id={self.id!r}, username={self.username!r}, type={self.type})"

    def to_dict(self):
        return {
            "type": self.type,
            "username": self.username,
            "url": self.url,
            "id": self.id,
            "profile_pic_url": self.profile_pic_url,
        }
