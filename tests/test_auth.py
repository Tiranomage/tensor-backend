import pytest
from httpx import AsyncClient

# from app.main import app
#
# @pytest.mark.anyio
# async def test_root():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Tomato"}

# if __name__ == '__main__':
#     unittest.main()
import pytest
from sqlalchemy import insert, select


from conftest import client, async_session_maker


def test_register():
    response = client.post("/auth/register", json={
        "email": "string",
        "password": "string",
        # "is_active": True,
        # "is_superuser": False,
        # "is_verified": False,
        # "username": "string",
        # "role_id": 1
    })

    response = client.post("/auth/register", json={
        "email": "string",
        "password": "string",
        # "is_active": True,
        # "is_superuser": False,
        # "is_verified": False,
        # "username": "string",
        # "role_id": 1
    })

    assert response.status_code == 201
