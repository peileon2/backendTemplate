from typing import List, Any
from fastapi import APIRouter, HTTPException, status, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.db import get_async_session
from app.models.user import User
from app.api.deps import current_active_user
from app.controller.baseRateControllers import (
    BaseRateController,
)  # 使用你优化后的控制器
from app.controller.deliveryControllers import AssembleController
from app.schemas.fedex.base_rate_schema import (
    BaseRateCreate,
    BaseRateUpdate,
    BaseRateBase,
)
from slowapi import Limiter
from slowapi.util import get_remote_address

# 初始化速率限制器
limiter = Limiter(key_func=get_remote_address)
router = APIRouter()


# 根据delivery_id获取BASE-RATE
@router.get("/{delivry_id}/{id}", response_model=BaseRateBase)
async def get_base_rate_by_id(
    delivry_id: int,
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
) -> BaseRateBase:
    assemble_controller = AssembleController(session=session, user_id=user.id)
    if not await assemble_controller.is_in_user(id=delivry_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wrong id")
    base_rate_controller = BaseRateController(session=session, delivery_id=delivry_id)
    base_rate = await base_rate_controller.get(id=id)
    if base_rate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="BaseRate not found"
        )
    return base_rate


# 创建新的BASE-RATE
@router.post(
    "/{delivry_id}", response_model=BaseRateBase, status_code=status.HTTP_201_CREATED
)
@limiter.limit("5/minute")  # 限制为每分钟5次请求
async def create_base_rate(
    request: Request,
    delivry_id: int,
    base_rate: BaseRateCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    assemble_controller = AssembleController(session=session, user_id=user.id)
    if not await assemble_controller.is_in_user(id=delivry_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="wrong delivery id"
        )
    base_rate_controller = BaseRateController(session=session, delivery_id=delivry_id)
    new_base_rate = await base_rate_controller.create(obj_in=base_rate)
    if new_base_rate is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="BaseRate creation failed"
        )
    return new_base_rate


# 更新BASE-RATE
@router.put("/{delivry_id}/{id}", response_model=BaseRateBase)
async def update_base_rate(
    delivry_id: int,
    id: int,
    base_rate: BaseRateUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    assemble_controller = AssembleController(session=session, user_id=user.id)
    if not await assemble_controller.is_in_user(id=delivry_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wrong id")
    base_rate_controller = BaseRateController(session=session, delivery_id=delivry_id)
    updated_base_rate = await base_rate_controller.update(id=id, obj_in=base_rate)
    if updated_base_rate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BaseRate not found or update failed",
        )
    return updated_base_rate


# 删除BASE-RATE
@router.delete("/{delivry_id}/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_base_rate(
    delivry_id: int,
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    assemble_controller = AssembleController(session=session, user_id=user.id)
    if not await assemble_controller.is_in_user(id=delivry_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wrong id")
    base_rate_controller = BaseRateController(session=session, delivery_id=user.id)
    success = await base_rate_controller.remove(id=id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BaseRate not found or deletion failed",
        )
    return None


# 批量查询BASE-RATE
@router.get("/{delivery_id}", status_code=status.HTTP_200_OK)
async def get_base_rate_list(
    delivery_id: int,
    page: int = 1,
    page_size: int = 10,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    """
    Retrieve a list of BaseRate objects for the given delivery_id, with pagination.
    """
    assemble_controller = AssembleController(session=session, user_id=user.id)

    # Check if the delivery_id belongs to the current user
    if not await assemble_controller.is_in_user(id=delivery_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wrong id")

    base_rate_controller = BaseRateController(session=session, delivery_id=delivery_id)

    # Fetch the BaseRate list with pagination
    total_count, base_rates = await base_rate_controller.get_list(
        page=page, page_size=page_size
    )

    # Handle case when no results are found
    if total_count == 0 or not base_rates:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="BaseRate not found"
        )

    # Return the total count and the list of BaseRate objects
    return {
        "total_count": total_count,
        "base_rates": base_rates,
    }
