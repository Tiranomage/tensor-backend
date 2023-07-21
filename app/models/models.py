import uuid
from datetime import datetime
from enum import Enum
from typing import List

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import ForeignKey
from sqlalchemy import String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship


class MessageType(Enum):
    # Похоже, более правильно указывать ссылку на сообщение, на которо отвечаем. А не тип
    # reply: str = "reply"
    text: str = "text"
    link: str = "link"
    geo: str = "geo"


class ChatType(Enum):
    # Личная переписка
    private: str = "private"
    # Группа по интересам
    group: str = "group"
    # Канал - можно подписаться и читать чужие мысли
    channel: str = "channel"
    # Событие
    event: str = "event"


class UserRole(Enum):
    user: str = "user"
    admin: str = "admin"
    moderator: str = "moderator"


# Base = declarative_base()
class Base(DeclarativeBase):
    pass


class User(Base, SQLAlchemyBaseUserTableUUID):
    __tablename__ = 'users'
    # username: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    external: Mapped[dict] = mapped_column(JSONB, default=lambda: {})
    # full_name: Mapped[str] = mapped_column(String(length=320))
    # birth_date: Mapped[date] = mapped_column(Date)
    # photo: Mapped[str] = mapped_column(String(length=320))
    # description: Mapped[str] = mapped_column(String(length=1024))
    # status: Mapped[str] = mapped_column(String(length=320))
    # emoji_status: Mapped[str | None] = mapped_column(String(length=64))
    # last_login: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    messages: Mapped[list["Message"]] = relationship("Message", back_populates="user", lazy="dynamic")
    chats: Mapped[List["Chat"]] = relationship(back_populates="users", secondary='user_chats', lazy="dynamic")
    tags: Mapped[List["Tag"]] = relationship(back_populates="users", secondary='user_tags', lazy="dynamic")

    user_chats: Mapped[list["UserChats"]] = relationship("UserChats", back_populates="user", lazy="dynamic")
    user_tags: Mapped[list["UserTags"]] = relationship("UserTags", back_populates="user", lazy="dynamic")


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    parent_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("chats.id"), nullable=True)
    type: Mapped[ChatType] = mapped_column(String(length=320), nullable=False)
    external: Mapped[dict] = mapped_column(JSONB, default=lambda: {})

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    messages: Mapped[list["Message"]] = relationship("Message", back_populates="chat", lazy="dynamic")
    users: Mapped[List["User"]] = relationship(back_populates="chats", secondary='user_chats', lazy="dynamic")
    tags: Mapped[List["Tag"]] = relationship(back_populates="chats", secondary='chat_tags', lazy="dynamic")

    user_chats: Mapped[list["UserChats"]] = relationship("UserChats", back_populates="chat", lazy="dynamic")
    chat_tags: Mapped[list["ChatTags"]] = relationship("ChatTags", back_populates="chat", lazy="dynamic")


class UserChats(Base):
    __tablename__ = "user_chats"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id"), nullable=False)
    chat_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("chats.id"), nullable=False)
    role: Mapped[UserRole] = mapped_column(String(length=320), default=UserRole.user, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="user_chats")
    chat: Mapped["Chat"] = relationship("Chat", back_populates="user_chats")


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    parent_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("messages.id"), nullable=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id"), nullable=False)
    chat_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("chats.id"), nullable=False)
    type: Mapped[MessageType] = mapped_column(String(length=320), nullable=False)
    external: Mapped[dict] = mapped_column(JSONB, default=lambda: {})

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="messages")
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    category_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("categories.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    category: Mapped["Category"] = relationship("Category", back_populates="tags")
    users: Mapped[List["User"]] = relationship(back_populates="tags", secondary='user_tags', lazy="dynamic")
    chats: Mapped[List["Chat"]] = relationship(back_populates="tags", secondary='chat_tags', lazy="dynamic")

    user_tags: Mapped[list["UserTags"]] = relationship("UserTags", back_populates="tag")
    chat_tags: Mapped[list["ChatTags"]] = relationship("ChatTags", back_populates="tag")


class UserTags(Base):
    __tablename__ = "user_tags"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id"), nullable=False)
    tag_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("tags.id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="user_tags")
    tag: Mapped["Tag"] = relationship("Tag", back_populates="user_tags")


class ChatTags(Base):
    __tablename__ = "chat_tags"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    chat_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("chats.id"), nullable=False)
    tag_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("tags.id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    chat: Mapped["Chat"] = relationship("Chat", back_populates="chat_tags")
    tag: Mapped["Tag"] = relationship("Tag", back_populates="chat_tags")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(length=320), unique=True, nullable=False)
    external: Mapped[dict] = mapped_column(JSONB, default=lambda: {})

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    tags: Mapped[list["Tag"]] = relationship("Tag", back_populates="category")
