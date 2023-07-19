import datetime
import uuid
from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str
    external: dict | None = None
    # fullname: str
    # birthdate: datetime.date


class UserCreate(schemas.BaseUserCreate):
    username: str
    external: dict | None = None
    # fullname: str
    # birthdate: datetime.date


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str]
    external: dict | None = None
    # fullname: Optional[str]
    # birthdate: Optional[datetime.date]