from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import false, func, true

from server.database import Base
from server.extensions import db
from server.users.models import User

if TYPE_CHECKING:
    from server.social_accounts.models import SocialAccount


class MonitoredUser(Base):
    __tablename__ = "monitored_users"

    name: Mapped[str]
    email: Mapped[str]
    is_approved: Mapped[bool] = mapped_column(server_default=false())
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="monitored_users")

    social_accounts: Mapped[List["SocialAccount"]] = relationship(
        "SocialAccount", back_populates="monitored_user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"MonitoredUser(id={self.id!r}, name={self.name!r}, email={self.email})"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "accounts": list(map(lambda acc: acc.to_dict(), self.social_accounts)),
        }
