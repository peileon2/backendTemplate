from typing import List
from app.controller.sku_controllers import SkuController
from app.schemas.sku_schema import SkuBase, SkuCreate, SkuUpdate
from fastapi import APIRouter, Query, HTTPException, status, Depends
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.db import get_session

router = APIRouter()


# 根据id获取sku
@router.get("/{id}", response_model=SkuBase)
async def get_sku_by_id(id: int, session: AsyncSession = Depends(get_session)) -> Any:
    sku_controller = SkuController(session=session)
    return await sku_controller.get(id=id)
