from sqlalchemy.ext.asyncio import AsyncSession

from app.config import app_settings
from app.models.models import Category

categories = [
    {
        'id': app_settings.USER_CATEGORY,
        'title': 'Пользовательская',
        'external': {},
    }
]

tags = [
    # {
    #     # 'id': '',
    #     'category_id': app_settings.USER_CATEGORY,
    #     'title': '',
    # }
]


async def seed_category(session: AsyncSession):
    for item in categories:
        category = await session.get(Category, item['id'])
        if category:
            continue
        session.add(Category(**item))
    await session.commit()
