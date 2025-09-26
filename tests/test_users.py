import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from main import app

client = TestClient(app)


@pytest.mark.anyio
async def test_login(client: AsyncClient):
    """Проверка успешной аутентификации пользователя и установки куков."""

    response = await client.post('/login', json={'email': "john1.doe@example.com", 'password': "password"})
    assert response.status_code == 200
    cookies = response.cookies
    assert 'session_token' in cookies.keys() and len(cookies['session_token']) > 0


@pytest.mark.anyio
async def test_get_current_user(client: AsyncClient):
    """Проверка получения текущего пользователя."""

    response = await client.post('/login', json={'email': "john1.doe@example.com", 'password': "password"})
    response = await client.get('/current', cookies={"session_token": response.cookies.get("session_token")})
    assert response.status_code == 200
    result = response.json()
    assert result['email'] == "john1.doe@example.com"


@pytest.mark.anyio
async def test_logout(client: AsyncClient):
    """Проверка выхода пользователя."""

    response = await client.post('/logout')
    assert response.status_code == 200
    assert response.json() == {"status": "logout success"}
