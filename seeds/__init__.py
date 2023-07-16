from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import UserChats, User, Chat
from seeds.const import password, created_at, today, dt_format, dt_fields, dt_fields2
from seeds.messages import get_messages
from seeds.user_chats import users, chats, user_chats


async def seed(session: AsyncSession):
    """
    Заполняем базу тестовыми данными. Эти же данные можно предварительно выгрузить на прод, как демонстрационные
    :param session:
    :return:
    """
    for item in users:
        item = item | dt_fields
        session.add(User(**item))
    await session.commit()

    for item in chats:
        item = item | dt_fields
        session.add(Chat(**item))
    await session.commit()

    for item in user_chats:
        item = item | dt_fields2
        session.add(UserChats(**item))
    await session.commit()

    await get_messages(session)