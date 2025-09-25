from fastapi import APIRouter, Depends, HTTPException, Path, Query
from starlette.responses import Response

from auth import hash_password, require_admin
from models import User
from schemas import (PaginatedMetaDataModel, PrivateCreateUserModel,
                     PrivateDetailUserResponseModel,
                     PrivateUsersListResponseModel, UsersListElementModel)

router = APIRouter(prefix="/private/users", tags=["admin"])


@router.get("/list", response_model=PrivateUsersListResponseModel)
async def private_list_users(page: int = Query(1, ge=1), size: int = Query(10, le=100),
                             _: User = Depends(require_admin)):
    """Список пользователей для администратора."""

    skip = (page - 1) * size
    users = await User.all().offset(skip).limit(size)
    total_count = await User.all().count()
    data = []
    for user in users:

        data_up = UsersListElementModel(id=user.id, first_name=user.first_name,
                                        last_name=user.last_name, email=user.email)

        data.append(data_up)
    pagination_meta = PaginatedMetaDataModel(total=total_count, page=page, size=size)

    return PrivateUsersListResponseModel(data=data, meta=pagination_meta)


@router.get("/info/{pk}", response_model=PrivateDetailUserResponseModel)
async def private_info_user(pk: int, _: User = Depends(require_admin)):
    """Просмотр полных данных о пользователе для администратора."""

    user = await User.get_or_none(id=pk)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/create", response_model=PrivateDetailUserResponseModel, status_code=201)
async def create_user(create_data: PrivateCreateUserModel, _: User = Depends(require_admin)):
    """Создание пользователя для администратора."""

    hashed_password = hash_password(create_data.password)
    new_user = await User.create(**create_data.dict(exclude={'password'}), password_hash=hashed_password)
    return new_user


@router.delete("/del/{pk}", status_code=204)
async def delete_user(pk: int = Path(...), no_del: User = Depends(require_admin)):
    """Удаление пользователя для администратора."""

    try:
        if no_del.id == pk:
            raise HTTPException(status_code=500, detail="Вы не можете удалить сами себя")
        deleted_count = await User.filter(id=pk).delete()
    except Exception as f:
        print(f)
        raise HTTPException(status_code=500, detail="Что-то пошло не так, мы уже исправляем эту ошибку")
    else:
        if deleted_count > 0:
            return Response(status_code=204)
        else:
            raise HTTPException(status_code=500, detail="Что-то пошло не так, мы уже исправляем эту ошибку")


@router.patch("/updata/{pk}", response_model=PrivateDetailUserResponseModel)
async def patch_user(pk: int, update_data: PrivateCreateUserModel, _: User = Depends(require_admin)):
    """Обновление пользователя для администратора."""

    user = await User.get_or_none(id=pk)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_fields = update_data.dict(exclude_unset=True)
    if 'password' in updated_fields:
        updated_fields['password_hash'] = hash_password(updated_fields.pop('password'))
    await user.update_from_dict(updated_fields).save()
    return user
