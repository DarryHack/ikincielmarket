"""SQLAlchemy 2.x stilinde modeller."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional, List
import secrets

from flask import current_app
from flask_login import UserMixin
from sqlalchemy import String, Integer, Text, ForeignKey, DateTime, Numeric, Boolean, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


def _now() -> datetime:
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now, nullable=False)

    listings: Mapped[List["Listing"]] = relationship(
        back_populates="seller", cascade="all, delete-orphan"
    )
    favorites: Mapped[List["Favorite"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    sent_messages: Mapped[List["Message"]] = relationship(
        foreign_keys="Message.sender_id", back_populates="sender", cascade="all, delete-orphan"
    )
    received_messages: Mapped[List["Message"]] = relationship(
        foreign_keys="Message.receiver_id", back_populates="receiver", cascade="all, delete-orphan"
    )

    def set_password(self, plain: str) -> None:
        # pbkdf2:sha256 — macOS sistem Python'unda hashlib.scrypt olmadığı için
        self.password_hash = generate_password_hash(plain, method="pbkdf2:sha256")

    def check_password(self, plain: str) -> bool:
        return check_password_hash(self.password_hash, plain)

    # E-posta şifre sıfırlama token'ı (HMAC tabanlı, jwt'siz)
    def generate_reset_token(self, expires_in_seconds: int = 1800) -> str:
        from itsdangerous import URLSafeTimedSerializer
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt="password-reset")
        return s.dumps({"uid": self.id})

    @staticmethod
    def verify_reset_token(token: str, max_age: int = 1800) -> Optional["User"]:
        from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt="password-reset")
        try:
            data = s.loads(token, max_age=max_age)
        except (BadSignature, SignatureExpired):
            return None
        return db.session.get(User, data.get("uid"))

    def avatar_url(self) -> str:
        if self.avatar:
            return f"/static/uploads/avatars/{self.avatar}"
        # Varsayılan: initials placeholder (dış servis yok — kendi static'imiz)
        return "/static/img/default-avatar.svg"

    def has_favorited(self, listing_id: int) -> bool:
        return db.session.query(
            db.exists().where((Favorite.user_id == self.id) & (Favorite.listing_id == listing_id))
        ).scalar()

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Category(db.Model):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)

    listings: Mapped[List["Listing"]] = relationship(back_populates="category")

    def __repr__(self) -> str:
        return f"<Category {self.name}>"


class Listing(db.Model):
    __tablename__ = "listing"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(140), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)  # active|sold|hidden
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now, nullable=False, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=False)

    seller: Mapped["User"] = relationship(back_populates="listings")
    category: Mapped["Category"] = relationship(back_populates="listings")
    favorited_by: Mapped[List["Favorite"]] = relationship(
        back_populates="listing", cascade="all, delete-orphan"
    )
    messages: Mapped[List["Message"]] = relationship(
        back_populates="listing", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_listing_search", "title", "description"),
    )

    def image_url(self) -> str:
        if self.image:
            return f"/static/uploads/listings/{self.image}"
        return "/static/img/no-image.svg"

    def __repr__(self) -> str:
        return f"<Listing {self.id} {self.title!r}>"


class Favorite(db.Model):
    __tablename__ = "favorite"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    listing_id: Mapped[int] = mapped_column(ForeignKey("listing.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now, nullable=False)

    user: Mapped["User"] = relationship(back_populates="favorites")
    listing: Mapped["Listing"] = relationship(back_populates="favorited_by")

    __table_args__ = (UniqueConstraint("user_id", "listing_id", name="uq_user_listing"),)

    def __repr__(self) -> str:
        return f"<Favorite u={self.user_id} l={self.listing_id}>"


class Message(db.Model):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now, nullable=False, index=True)

    sender_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    listing_id: Mapped[Optional[int]] = mapped_column(ForeignKey("listing.id"), nullable=True)

    sender: Mapped["User"] = relationship(foreign_keys=[sender_id], back_populates="sent_messages")
    receiver: Mapped["User"] = relationship(foreign_keys=[receiver_id], back_populates="received_messages")
    listing: Mapped[Optional["Listing"]] = relationship(back_populates="messages")

    def __repr__(self) -> str:
        return f"<Message {self.id} {self.sender_id}->{self.receiver_id}>"
