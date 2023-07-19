import uuid

from fastapi import FastAPI, APIRouter, Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import app_settings
from app.models.db import User, get_async_session
from app.shemas.user import UserRead, UserCreate, UserUpdate
from .manager import get_user_manager
from ..crud.crud_category import crud_tag, crud_user_tags
from ..shemas import category as search_schemas


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=app_settings.JWT_SECRET, lifetime_seconds=3600)


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


additional_users_router = APIRouter(prefix="/users", tags=["users"])


@additional_users_router.get("/tags")
async def user_tags(
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    tags_obj = user.tags[offset:offset+limit]
    return tags_obj


@additional_users_router.put("/tags", response_model=list[search_schemas.Tag])
async def create_user_tags(
        tags_id: list[uuid.UUID],
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    tags_obj = []

    for tag_id in tags_id:
        tag_obj = await crud_tag.get(session, model_id=tag_id)
        user_tags_create = search_schemas.UserTagsCreate(user_id=user.id, tag_id=tag_obj.id)
        await crud_user_tags.create(session, obj_in=user_tags_create)
        tags_obj.append(tag_obj)

    return tags_obj


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

    app.include_router(
        fastapi_users.get_users_router(UserRead, UserUpdate),
        prefix="/users",
        tags=["users"],
    )

    app.include_router(
        additional_users_router,
        prefix="/users",
        tags=["users"]
    )
