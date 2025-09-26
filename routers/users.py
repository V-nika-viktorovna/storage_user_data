from datetime import timedelta

from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response

from auth import authenticate_user, create_access_token, get_current_user
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from models import User
from schemas import (CurrentUserResponseModel, LoginModel,
                     PaginatedMetaDataModel, UpdateUserModel,
                     UsersListElementModel, UsersListResponseModel)

router = APIRouter(tags=["user"])


@router.post("/login", response_model=CurrentUserResponseModel)
async def login(response: Response, login_model: LoginModel):

    user = await authenticate_user(login_model.email, login_model.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user['email']}, expires_delta=access_token_expires
    )
    print(access_token)

    response.set_cookie(key="session_token",
                        value=f"Bearer {access_token}",
                        httponly=True, secure=True, samesite='lax',
                        max_age=int(access_token_expires.total_seconds()))

    return user


@router.get("/current", response_model=CurrentUserResponseModel)
async def current_user(current_user: User = Depends(get_current_user)):
    """Просмотр текущего пользователя."""

    return current_user


@router.patch("/edit", response_model=CurrentUserResponseModel)
async def edit_user(update_data: UpdateUserModel, current_user: User = Depends(get_current_user)):
    """Редактирование текущего пользователя."""

    for field in update_data.__fields_set__:
        setattr(current_user, field, getattr(update_data, field))
    await current_user.save()
    return current_user


@router.get("/", response_model=UsersListResponseModel)
async def paginate_users(page: int = Query(1, ge=1), size: int = Query(10, le=100)):
    """Отображение пользователяей с пагинацией."""

    skip = (page - 1) * size
    users = await User.all().offset(skip).limit(size)
    total_count = await User.all().count()
    data = []
    for user in users:
        data_up = UsersListElementModel(id=user.id, first_name=user.first_name,
                                        last_name=user.last_name, email=user.email)

        data.append(data_up)

    pagination_meta = PaginatedMetaDataModel(total=total_count, page=page, size=size)
    return UsersListResponseModel(data=data, meta=pagination_meta)


@router.post("/logout", summary="Logout the current session")
async def logout(response: Response):

    response.delete_cookie("session_token")
    return {"status": "logout success"}
