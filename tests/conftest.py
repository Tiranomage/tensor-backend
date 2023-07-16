import asyncio
from typing import AsyncGenerator

import alembic
import pytest
from alembic.config import Config
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config import test_database_settings
from app.main import app
from app.models.db import get_async_session
from app.models.models import Base
from seeds import seed

metadata = Base.metadata
engine_test = create_async_engine(test_database_settings.database_url, echo=test_database_settings.ECHO, future=True,
                                  poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session
client = TestClient(app)


# Apply migrations at beginning and end of testing session
@pytest.fixture(autouse=True, scope="session")
def prepare_database():  # session: AsyncSession = Depends(override_get_async_session)):
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", "FASTAPI_TESTING")
    alembic.command.upgrade(config, "head")
    yield
    # config.set_main_option("sqlalchemy.url", "FASTAPI_TESTING")
    # alembic.command.downgrade(config, "base")


@pytest.fixture(autouse=True, scope="session")
async def prepare_database2():  # session: AsyncSession = Depends(override_get_async_session)):
    async with async_session_maker() as session:
        await seed(session)


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
