from typing import List
from fastapi import APIRouter, Query, HTTPException, status, Depends, Request
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.db import get_async_session
from app.api.deps import current_active_user
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy import select
from app.models.user import User
from app.schemas.delivery_schema import Ahs, AhsCreate, AhsUpdate
from app.controller.deliveryControllers import AHSController

# 初始化速率限制器
limiter = Limiter(key_func=get_remote_address)
router = APIRouter()


### AHS等controller需要修改 不需要userid
# 根据id获取Assemble
@router.get("/{id}", response_model=Ahs)
async def get_ahs_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
) -> Ahs:
    sku_controller = AHSController(session=session, user_id=user.id)
    sku = await sku_controller.get(id=id)
    if sku is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="SKU not found"
        )
    return sku


@router.post("/", response_model=Ahs, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")  # 限制为每分钟5次请求
async def create_ahs(
    request: Request,
    ahs_create: AhsCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    ahs_controller = AHSController(session=session, user_id=user.id)
    ahs = await ahs_controller.create(obj_in=ahs_create)
    print(ahs)
    if ahs is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="ahs created failed"
        )
    return ahs
