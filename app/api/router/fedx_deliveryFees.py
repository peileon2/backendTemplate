from typing import List
from fastapi import APIRouter, Query, HTTPException, status, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.db import get_async_session
from app.api.deps import current_active_user
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy import select
from app.models.user import User
from app.schemas.fedex.delivery_schema import (
    AssembleDeliveryFees,
    AssembleDeliveryFeesChildren,
    AssembleDeliveryFeesUpdate,
)
from app.controller.deliveryControllers import (
    AssembleController,
)

# 初始化速率限制器
limiter = Limiter(key_func=get_remote_address)
router = APIRouter()


# 根据id获取Assemble
@router.get("/{id}/get", response_model=AssembleDeliveryFees)
async def get_assemble_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
) -> AssembleDeliveryFees:
    assemble_controller = AssembleController(session=session, user_id=user.id)
    assemble = await assemble_controller.select_with_children(id=id)
    print(assemble)
    if assemble is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assemble not found"
        )
    return assemble


# 创建带有子项的Assemble
@router.post(
    "/create", status_code=status.HTTP_201_CREATED
)  # , response_model=AssembleDeliveryFees
@limiter.limit("5/minute")  # 限制为每分钟5次请求
async def create_assemble_with_children(
    request: Request,
    assemble: AssembleDeliveryFeesChildren,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    assemble_controller = AssembleController(session=session, user_id=user.id)
    assemble_data = await assemble_controller.create_with_children(obj_in=assemble)
    print(assemble)
    print(type(assemble))
    if assemble_data is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Assemble with children creation failed",
        )
    return None


# 根据id删除Assemble
@router.delete("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_assemble_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    assemble_controller = AssembleController(session=session, user_id=user.id)
    assemble = await assemble_controller.select_with_children(id=id)

    if assemble is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assemble not found"
        )

    # 调用控制器的删除方法
    await assemble_controller.delete_with_children(id=id)
    return None  # 删除操作成功返回空


# 根据id更新Assemble
@router.put("/{id}/update")
async def update_assemble_by_id(
    id: int,
    assemble_update: AssembleDeliveryFeesUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    assemble_controller = AssembleController(session=session, user_id=user.id)

    # 查找要更新的Assemble记录
    assemble = await assemble_controller.select_with_children(id=id)

    if assemble is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assemble not found"
        )

    # 调用控制器的更新方法
    updated_assemble = await assemble_controller.update_with_children(
        obj_in=assemble_update, id=id
    )

    return None


# # 根据id获取Assemble,并算出fedex价格
# @router.get("/{id}", response_model=AssembleDeliveryFees)
# async def get_assemble_by_id(
#     id: int,
#     session: AsyncSession = Depends(get_async_session),
#     user: User = Depends(current_active_user),
# ) -> AssembleDeliveryFees:
#     assemble_controller = AssembleController(session=session, user_id=user.id)
#     assemble = await assemble_controller.select_with_children(id=id)
#     if assemble is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Assemble not found"
#         )

#     return assemble
