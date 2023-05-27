from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.database import Base
from server.users.models import User


class SocialAuth(Base):
    __tablename__ = "social_auths"

    username: Mapped[str]
    auth_id: Mapped[str]
    access_token: Mapped[str]
    expires_in: Mapped[int]
    type: Mapped[str]

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="social_auths")

    def __repr__(self) -> str:
        return f"SocialAuth(id={self.id!r}, username={self.username!r})"
