import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin, exceptions
from fastapi_users.db import SQLAlchemyUserDatabase

from app.config import app_settings
from app.models.db import User, get_user_db
from app.shemas.user import EmailOrPhone


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = app_settings.USER_MANAGER_SECRET
    verification_token_secret = app_settings.USER_MANAGER_SECRET

    async def get_by_email(self, user_email: str):
        """
        Переопределяем функцию проверки email
        добавляем проверку Телефона
        """
        try:
            validated = EmailOrPhone(email=user_email)
        except Exception:
            raise exceptions.UserNotExists()

        user = await self.user_db.get_by_email(validated.email)

        if user is None:
            raise exceptions.UserNotExists()

        return user

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
