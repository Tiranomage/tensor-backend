import datetime

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import String, DATE
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base, SQLAlchemyBaseUserTableUUID):
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    fullname: Mapped[str] = mapped_column(String(length=320), unique=False, index=False, nullable=False)
    birthdate: Mapped[datetime.date] = mapped_column(DATE)
