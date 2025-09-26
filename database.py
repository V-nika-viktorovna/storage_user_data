from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise

from config import DATABASE_URL, toroise_orm

engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db(app):
    register_tortoise(
        app,
        config=toroise_orm,
        generate_schemas=True,
        add_exception_handlers=True,
    )


# Проверка подключение к базе данных
async def check_database_connection():
    try:
        await Tortoise.init(config=toroise_orm)
        print("Подключение к базе успешно!")
    except Exception as e:
        print(f"Подключение к базе Failed: {e}")
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(check_database_connection())
