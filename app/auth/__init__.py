import uuid
from typing import Optional

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import app_settings
from app.models.db import User, get_async_session
from app.shemas.user import UserRead, UserCreate, EmailOrPhone
from app.auth.manager import get_user_manager
from app.crud.crud_category import crud_tag, crud_user_tags
from app.shemas import category as search_schemas


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=app_settings.JWT_SECRET, lifetime_seconds=app_settings.JWT_LIFETIME)


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

current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True)

additional_users_router = APIRouter(prefix="/current", tags=["current"])


@additional_users_router.get("", response_model=UserRead)
async def user(user: User = Depends(current_user)):
    return user


@additional_users_router.get("/tags", response_model=list[search_schemas.Tag])
async def user_tags(
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    tags_obj = (await session.scalars(user.tags.statement.offset(offset).limit(limit))).all()
    return tags_obj


@additional_users_router.post("/tags", response_model=list[search_schemas.Tag])
async def update_user_tags(
        tags: list[search_schemas.TagCreate],
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    tags_obj = await crud_tag.exist_create(session, tags=tags)

    for tag in tags_obj:
        user_tags_create = search_schemas.UserTagsCreate(user_id=user.id, tag_id=tag.id)
        await crud_user_tags.create(session, obj_in=user_tags_create)

    return tags_obj


auth_router = APIRouter()


@auth_router.post("/find", response_model=UserRead, response_model_include={"email", "id"}, )
async def auth_find(
        email: EmailOrPhone,
        session: AsyncSession = Depends(get_async_session)
):
    statement = select(User).where(
        func.lower(User.email) == func.lower(email.email)
    )
    results = await session.execute(statement)
    user = results.unique().scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="USER_NOT_EXISTS")
    return user


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
        prefix="/auth",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_verify_router(UserRead),
        prefix="/auth",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth",
        tags=["auth"],
    )

    # app.include_router(
    #     fastapi_users.get_users_router(UserRead, UserUpdate),
    #     prefix="/users",
    #     tags=["users"],
    # )

    app.include_router(
        auth_router,
        prefix="/auth",
        tags=["auth"]
    )

    app.include_router(
        additional_users_router,
    )
