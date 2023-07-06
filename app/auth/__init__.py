import uuid

from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

from app.config import JWT_SECRET
from app.models.db import User
from app.shemas.user import UserRead, UserCreate, UserUpdate
from .manager import get_user_manager


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=JWT_SECRET, lifetime_seconds=3600)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)


def include_auth_router(app: FastAPI) -> None:
    """
    Добавляем в приложение роуты авторизации и регистрации
    """
    app.include_router(
        fastapi_users.get_auth_router(auth_backend),
        prefix="/auth/jwt",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/auth1",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_verify_router(UserRead),
        prefix="/auth2",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth3",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_users_router(UserRead, UserUpdate),
        prefix="/users",
        tags=["users"],
    )
