from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import false, func, true


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        unique=True,
        type_=UUID(as_uuid=False),
        server_default=text("uuid_generate_v4()"),
    )


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


class Post(Base):
    __tablename__ = "posts"

    text: Mapped[str] = mapped_column(server_default=text("''"))
    date: Mapped[datetime]
    category: Mapped[str]
    probability: Mapped[float]

    social_account_id: Mapped[UUID] = mapped_column(ForeignKey("social_accounts.id"))
    social_account: Mapped["MonitoredUser"] = relationship(
        "SocialAccount", back_populates="posts"
    )

    def __repr__(self) -> str:
        return f"MonitoredUser(id={self.id!r}, username={self.username!r}, type={self.type})"
