import asyncio
from typing import Generator

import asyncpg
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from config import DATABASE_URL, toroise_orm
from main import app
from models import User
from schemas import LoginModel, UpdateUserModel

DB_URL = DATABASE_URL


@pytest_asyncio.fixture(autouse=True)
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="module")
async def db_connection():
    """Фикстура для создания пула подключений"""
    pool = await asyncpg.create_pool(toroise_orm)
    yield pool
    await pool.close()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest_asyncio.fixture(scope="module")
async def prepare_database(db_connection):
    """Предварительное создание пользователя в базе данных"""

    await User.create(first_name="John", last_name="Doe", email="john.doe@example.com", password="password")
    yield

    await User.filter().delete()


@pytest_asyncio.fixture(scope="module")
def test_user():
    return User(first_name="John", last_name="Doe", email="john.doe@example.com", password="password")


@pytest_asyncio.fixture(scope="module")
def test_login_model(prepare_database):
    """Фикстура для модели входа"""

    model = LoginModel(email="john.doe@example.com", password="password")

    yield dict(model)


@pytest_asyncio.fixture(scope="module")
def test_update_user_model():
    """фикстура для обновления пользователя."""

    model = UpdateUserModel(first_name='Jane', last_name='Smith', other_name="dfgh",
                            email='jane.smith@example.com', phone='+1234567890', birthday='1990-01-01')
    yield model
