from typing import List
from app.controller.sku_controllers import SkuController
from app.schemas.sku_schema import SkuBase, SkuCreate, SkuUpdate
from fastapi import APIRouter, Query, HTTPException, status, Depends, Request
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.db import get_async_session
from app.models.user import User
from app.api.deps import current_active_user
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.models.sku import Sku
from sqlalchemy import select

# 初始化速率限制器
limiter = Limiter(key_func=get_remote_address)
router = APIRouter()


# 根据id获取sku
@router.get("/{id}", response_model=SkuBase)
async def get_sku_by_id(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> SkuBase:
    sku_controller = SkuController(session=session)
    sku = await sku_controller.get(id=id)
    if sku is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="SKU not found"
        )
    return sku


# # 获取所有SKU,下方代码暂不写，因需要兼顾搜索选项
# @router.get("/", response_model=List[SkuBase])
# async def get_skus(session: AsyncSession = Depends(get_session)):
#     sku_controller = SkuController(session=session)
#     return await sku_controller.get_list(page=1, page_size=10, order=None)


@router.post("/", response_model=SkuBase, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")  # 限制为每分钟5次请求
async def create_sku(
    request: Request,
    sku: SkuCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    sku_controller = SkuController(session=session)
    sku = await sku_controller.create(obj_in=sku)
    if sku is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="SKU created failed"
        )
    return sku


# 更新SKU
@router.put("/{id}", response_model=SkuBase)
async def update_sku(
    id: int, sku: SkuUpdate, session: AsyncSession = Depends(get_async_session)
):
    sku_controller = SkuController(session=session)
    return await sku_controller.update(id=id, obj_in=sku)


# 删除SKU
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sku(id: int, session: AsyncSession = Depends(get_async_session)):
    sku_controller = SkuController(session=session)
    await sku_controller.remove(id=id)
    return None
