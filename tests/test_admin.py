import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from auth import hash_password
from main import app
from models import User

client = TestClient(app)


@pytest.mark.anyio
async def test_info_user_admin(client: AsyncClient):
    """Проверка получения полной информации о пользователе."""

    await User.create(first_name="John", last_name="Doe", email="john.doe@example.com",
                      password_hash=hash_password("password"))

    await User.create(first_name="John1", last_name="Doe", email="john1.doe@example.com",
                      password_hash=hash_password("password"), additional_info="Optional")

    test_user_admin = await User.create(first_name="Test", last_name="Test", email="test8@example.com",
                                        password_hash=hash_password("password"), is_admin=True)

    response = await client.post('/login', json={'email': test_user_admin.email, 'password': "password"})
    response = await client.get('/admin/private/users/info/2',
                                cookies={"session_token": response.cookies.get("session_token")})
    assert response.status_code == 200
    result = response.json()
    assert result['additional_info'] == "Optional"


@pytest.mark.anyio
async def test_delete_user(client: AsyncClient):
    """Проверка удаления пользователя не администратором."""

    response = await client.post('/login', json={'email': 'john.doe@example.com', 'password': "password"})
    response = await client.delete('/admin/private/users/del/2',
                                   cookies={"session_token": response.cookies.get("session_token")})
    assert response.status_code == 403


@pytest.mark.anyio
async def test_delete_user_admin(client: AsyncClient):
    """Проверка удаления пользователя администратором."""

    response = await client.post('/login', json={'email': 'test8@example.com', 'password': "password"})
    response = await client.delete('/admin/private/users/del/1',
                                   cookies={"session_token": response.cookies.get("session_token")})
    assert response.status_code == 204
