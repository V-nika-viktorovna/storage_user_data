import os

import pytest
from httpx import AsyncClient
from tortoise import Tortoise

from main import app

# @pytest_asyncio.fixture(autouse=True)
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()
#
#
# @pytest_asyncio.fixture(scope="module")
# async def db_connection():
#     """Фикстура для создания пула подключений"""
#     pool = await asyncpg.create_pool(toroise_orm)
#     yield pool
#     await pool.close()
#
#
# @pytest.fixture(scope="module")
# def client() -> Generator[TestClient, None, None]:
#     with TestClient(app) as c:
#         yield c
#
#
# @pytest_asyncio.fixture(scope="module")
# async def prepare_database(db_connection):
#     """Предварительное создание пользователя в базе данных"""
#
#     await User.create(first_name="John", last_name="Doe", email="john.doe@example.com", password="password")
#     yield
#
#     await User.filter().delete()
#
#
# @pytest_asyncio.fixture(scope="module")
# def test_user():
#     return User(first_name="John", last_name="Doe", email="john.doe@example.com", password="password")
#
#
# @pytest_asyncio.fixture(scope="module")
# def test_login_model(prepare_database):
#     """Фикстура для модели входа"""
#
#     model = LoginModel(email="john.doe@example.com", password="password")
#
#     yield dict(model)
#
#
# @pytest_asyncio.fixture(scope="module")
# def test_update_user_model():
#     """фикстура для обновления пользователя."""
#
#     model = UpdateUserModel(first_name='Jane', last_name='Smith', other_name="dfgh",
#                             email='jane.smith@example.com', phone='+1234567890', birthday='1990-01-01')
#     yield model

DB_URL = "sqlite://:memory:"


async def init_db(db_url, create_db: bool = False, schemas: bool = False) -> None:
    """Initial database connection"""
    await Tortoise.init(
        db_url=db_url, modules={"models": ["models"]}, _create_db=create_db
    )
    if create_db:
        print(f"Database created! {db_url=}")
    if schemas:
        await Tortoise.generate_schemas()
        print("Success to generate schemas")


async def init(db_url: str = DB_URL):
    await init_db(db_url, True, True)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        print("Client is ready")
        yield client


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await init()
    print(5)
    try:
        yield
    finally:
        if os.getenv('DROP_TESTING_DB'):
            print(3)
            await Tortoise._drop_databases()
        else:
            print(2323)
            await Tortoise.close_connections()
