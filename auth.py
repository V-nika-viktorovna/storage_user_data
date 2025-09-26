import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from starlette.requests import Request

from models import User, User_Pydantic

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def verify_password(plain_password: str, hashed_password: str | None) -> bool:
    """Функция принимает обычный пароль и хешированный пароль из базы данных
    и проверяет их соответствие друг другу."""
    print("проверка пароля")

    if hashed_password is None:
        print("пароля нет")
        return "пароля нет"

    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """Функция принимает обычный пароль и возвращает его хешированное представление,
    подходящее для хранения в базе данных."""

    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Функция создает JWT-токен на основе указанных данных и добавляет в него временное ограничение
    или используете заранее настроенное время истечения. Она подписывает токен с помощью секретного ключа
    и указанного алгоритма шифрования."""

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt


async def authenticate_user(user_email: str, password: str):
    """Функция получает пользователя по адресу электронной почты и проверяет пароль.
    Если пользователь не найден или пароль неверен, поднимает ошибку 401 Unauthorized."""

    user = await User.get(email=user_email)
    user_orm = await User_Pydantic.from_tortoise_orm(user)
    if user_orm:
        print("пользователь есть")
        print(user_orm.dict())

    if not user_orm:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    elif verify_password(password, user.password_hash) == "пароля нет":
        print("должен вернуть пользователя")
        return user_orm.dict()
    elif not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    else:
        return user_orm.dict()


async def get_current_user(request: Request):
    """Функция пытается расшифровать токен и получить оттуда идентификатор пользователя (субъекта).
    Если токен некорректен или истек, выдает ошибку 401 Unauthorized.
    Если всё прошло успешно, возвращает пользователя из базы данных."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = request.cookies.get("session_token")
        if not token:
            raise credentials_exception
        payload = jwt.decode(token.split()[1], os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await User.get(email=username)
    if user is None:
        raise credentials_exception
    return user


async def require_admin(user: User = Depends(get_current_user)):

    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")
    return user
