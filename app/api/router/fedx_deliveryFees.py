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
    AssembleDeliveryFeesCreate,
    AssembleDeliveryFeesChildren,
)
from app.controller.deliveryControllers import (
    AssembleController,
    DasController,
    BaseController,
    AHSController,
)

# 初始化速率限制器
limiter = Limiter(key_func=get_remote_address)
router = APIRouter()


# 根据id获取Assemble
@router.get("/{id}", response_model=AssembleDeliveryFees)
async def get_assemble_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
) -> AssembleDeliveryFees:
    assemble_controller = AssembleController(session=session, user_id=user.id)
    assemble = await assemble_controller.get(id=id)
    if assemble is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assemble not found"
        )
    return assemble


@router.post(
    "/", response_model=AssembleDeliveryFees, status_code=status.HTTP_201_CREATED
)
@limiter.limit("5/minute")  # 限制为每分钟5次请求
async def create_assemble(
    request: Request,
    assemble: AssembleDeliveryFeesCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    assemble_controller = AssembleController(session=session, user_id=user.id)
    assemble = await assemble_controller.create(obj_in=assemble)
    if assemble is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Assemble creation failed"
        )
    return assemble


# 创建带有子项的Assemble
@router.post(
    "/with-children",
    response_model=AssembleDeliveryFees,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/minute")  # 限制为每分钟5次请求
async def create_assemble_with_children(
    request: Request,
    assemble: AssembleDeliveryFeesChildren,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    assemble_controller = AssembleController(session=session, user_id=user.id)
    assemble = await assemble_controller.create_with_children(obj_in=assemble)
    if assemble is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Assemble with children creation failed",
        )
    return assemble


# 根据id获取Assemble,并算出fedex价格
@router.get("/{id}", response_model=AssembleDeliveryFees)
async def get_assemble_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
) -> AssembleDeliveryFees:
    assemble_controller = AssembleController(session=session, user_id=user.id)
    assemble = await assemble_controller.get(id=id)
    if assemble is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assemble not found"
        )

    return assemble
