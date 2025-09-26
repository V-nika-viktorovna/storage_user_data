from fastapi import FastAPI
from tortoise import Tortoise, run_async

from auth import hash_password
from config import toroise_orm
from models import User

app = FastAPI()


async def create_user(email: str, password: str, is_admin=True):
    """Функция создает пользователя с правами администратора."""

    await Tortoise.init(config=toroise_orm)
    hashed_password = hash_password(password)
    await User.create(email=email, password_hash=hashed_password, is_admin=is_admin)

    print(f'Пользователь {email} успешно создан!')
    await Tortoise.close_connections()

if __name__ == "__main__":
    email = input("Введите email в формате: ****@***.**: ")
    password = input("Введите пароль: ")
    run_async(create_user(email=email, password=password))
