import datetime
import uuid
from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str
    # fullname: str
    # birthdate: datetime.date


class UserCreate(schemas.BaseUserCreate):
    username: str
    # fullname: str
    # birthdate: datetime.date


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str]
    # fullname: Optional[str]
    # birthdate: Optional[datetime.date]