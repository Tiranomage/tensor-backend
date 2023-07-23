from app.crud.crud_base import CRUDBase
from app.models.models import User
from app.shemas.user import (
    UserCreate,
    UserUpdate
)


class CRUDUSer(CRUDBase[User, UserCreate, UserUpdate]):
    pass


crud_user = CRUDUSer(User)
