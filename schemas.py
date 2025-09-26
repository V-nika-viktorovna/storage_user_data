from datetime import date
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class LoginModel(BaseModel):
    email: str
    password: str


class CurrentUserResponseModel(BaseModel):
    """Модель используется для представления данных текущего зарегистрированного пользователя."""

    first_name: str | None
    last_name: str | None
    other_name: str | None
    email: EmailStr
    phone: str | None
    birthday: date | None
    is_admin: bool

    class Config:
        from_attributes = True


class CitiesHintModel(BaseModel):
    id: int
    name: str


class ErrorResponseModel(BaseModel):
    """Структура ошибок, используемых приложением."""

    code: int
    message: str


class CodelessErrorResponseModel(BaseModel):
    """Упрощенная версия предыдущей модели для ситуаций, когда ошибка не требует конкретного кода."""

    message: str


class HTTPValidationError(BaseModel):
    """Описание ошибок валидации, возникающих при обработке HTTP-запросов."""

    detail: List["ValidationError"]


class PaginatedMetaDataModel(BaseModel):
    """Постраничного вывода результатов."""

    total: int
    page: int
    size: int


class PrivateCreateUserModel(BaseModel):
    """Данные для создания приватного пользователя."""

    first_name: str | None
    last_name: str | None
    email: str
    is_admin: bool | None
    password: str | None
    other_name: Optional[str]
    phone: Optional[str]
    birthday: Optional[date]
    city: int | None
    additional_info: Optional[str]


class PrivateDetailUserResponseModel(BaseModel):
    """Детальная информация о пользователе."""

    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    other_name: Optional[str]
    email: str
    phone: Optional[str]
    birthday: Optional[date]
    city: int | None
    additional_info: Optional[str]
    is_admin: bool


class PrivateUpdateUserModel(BaseModel):
    """Модель для обновления данных приватного пользователя."""

    id: int
    first_name: str
    last_name: str
    other_name: Optional[str]
    email: str
    phone: Optional[str]
    birthday: Optional[date]
    city: int | None
    additional_info: Optional[str]
    is_admin: bool


class PrivateUsersListHintMetaModel(BaseModel):
    """Данные для списка пользователей с информацией о городах."""

    city: List[CitiesHintModel]


class PrivateUsersListMetaDataModel(BaseModel):
    """Содержит дополнительную информацию для списка приватных пользователей."""

    pagination: PaginatedMetaDataModel
    hint: PrivateUsersListHintMetaModel


class PrivateUsersListResponseModel(BaseModel):
    """Ответ сервера на запрос списка приватных пользователей."""

    data: List["UsersListElementModel"]
    meta: PaginatedMetaDataModel


class UpdateUserModel(BaseModel):
    """Частичное обновление публичного пользователя."""

    first_name: Optional[str]
    last_name: Optional[str]
    other_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    birthday: Optional[date]


class UpdateUserResponseModel(BaseModel):
    """Результат успешного обновления пользователя."""

    id: int
    first_name: str
    last_name: str
    other_name: Optional[str]
    email: str
    phone: Optional[str]
    birthday: Optional[date]

    class Config:
        from_attributes = True


class UsersListElementModel(BaseModel):
    """Элемент списка пользователей, содержащий минимально необходимую информацию."""

    id: int
    first_name: str | None
    last_name: str | None
    email: str


class UsersListMetaDataModel(BaseModel):
    """Метаданные для общего списка пользователей."""

    pagination: PaginatedMetaDataModel


class UsersListResponseModel(BaseModel):
    """Форматированный ответ сервера на запрос списка пользователей."""

    data: List[UsersListElementModel]
    meta: PaginatedMetaDataModel


class ValidationError(BaseModel):
    """Хранит информацию об ошибках валидации, возникших при проверке данных."""

    loc: List[str]
    msg: str
    type: str
