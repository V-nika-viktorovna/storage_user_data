
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from auth import hash_password
from main import app
from models import User

client = TestClient(app)

#
# @pytest.mark.asyncio
# async def test_login(prepare_database, client):
#     """Проверка успешной аутентификации пользователя и установки куков."""
#
#     response = client.post('/login', json={'email': 'john.doe@example.com', 'password': 'password'})
#     assert response.status_code == 200
#
#     cookies = response.cookies
#     assert 'session_token' in cookies.keys() and len(cookies['session_token']) > 0
#
#
# @pytest.mark.asyncio
# async def test_get_current_user(db_connection, client, test_user):
#     """Проверка получения текущего пользователя."""
#
#     #await User.create(first_name="John", last_name="Doe", email="john.doe@example.com", password="password")
#
#     response = client.get('/current', headers={'Authorization': f'Bearer fake_token'})
#     assert response.status_code == 200
#     result = response.json()
#     assert result['email'] == test_user.email
#
#
# @pytest.mark.asyncio
# async def test_edit_user(db_connection, client, test_update_user_model):
#     """Редактирование профиля пользователя."""
#
#     #await User.create(first_name="John", last_name="Doe", email="john.doe@example.com", password="password")
#
#     response = client.patch('/edit', json=test_update_user_model.dict(),
#                             headers={'Authorization': f'Bearer fake_token'})
#     assert response.status_code == 200
#     updated_user = response.json()
#     assert updated_user['first_name'] == test_update_user_model.first_name
#     assert updated_user['last_name'] == test_update_user_model.last_name


# @pytest.mark.asyncio
# async def test_paginate_users(client):
#     """Тестирование вывода списка пользователей с пагинацией."""
#
#     response = client.get('/?page=1&size=10')
#     assert response.status_code == 200
#     result = response.json()
#     assert isinstance(result, dict)
#     assert 'data' in result and 'meta' in result
#     assert isinstance(result['data'], list)
#     assert isinstance(result['meta'], dict)
#
#
# @pytest.mark.asyncio
# async def test_logout(client):
#     """Проверка выхода пользователя."""
#
#     response = client.post('/logout')
#     assert response.status_code == 200


@pytest.mark.anyio
async def test_login(client: AsyncClient):
    """Проверка успешной аутентификации пользователя и установки куков."""
    test_user = await User.create(first_name="John", last_name="Doe", email="john.doe@example.com",
                                  password_hash=hash_password("password"))
    response = await client.post('/login', json={'email': test_user.email, 'password': "password"})
    assert response.status_code == 200
    cookies = response.cookies
    assert 'session_token' in cookies.keys() and len(cookies['session_token']) > 0


@pytest.mark.anyio
async def test_get_current_user(client: AsyncClient):
    """Проверка получения текущего пользователя."""

    response = await client.post('/login', json={'email': "john.doe@example.com", 'password': "password"})
    response = await client.get('/current', cookies={"session_token": response.cookies.get("session_token")})
    assert response.status_code == 200
    result = response.json()
    assert result['email'] == "john.doe@example.com"


@pytest.mark.anyio
async def test_logout(client: AsyncClient):
    """Проверка выхода пользователя."""

    response = await client.post('/logout')
    assert response.status_code == 200
    assert response.json() == {"status": "logout success"}
