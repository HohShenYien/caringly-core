from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text

from server.database import Base
from server.social_accounts.models import SocialAccount


class Post(Base):
    __tablename__ = "posts"

    text: Mapped[str] = mapped_column(server_default=text("''"))
    date: Mapped[datetime]
    category: Mapped[str]
    probability: Mapped[float]

    social_account_id: Mapped[UUID] = mapped_column(ForeignKey("social_accounts.id"))
    social_account: Mapped["SocialAccount"] = relationship(
        "SocialAccount", back_populates="posts"
    )

    def __repr__(self) -> str:
        return f"MonitoredUser(id={self.id!r}, text={self.text!r}, category={self.category})"