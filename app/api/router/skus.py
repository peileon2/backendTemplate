from typing import List
from app.controller.sku_controllers import sku_controller
from app.schemas.sku_schema import SkuBase, SkuCreate
from fastapi import APIRouter
from typing import Any

router = APIRouter()


# 根据id获取sku
@router.get("/{id}", response_model=SkuBase)
async def get_sku_by_id(id: int) -> Any:
    return await sku_controller.get(id=id)


@router.post("/", response_model=SkuCreate)
async def create_item(sku_in: SkuCreate) -> Any:
    sku = await sku_controller.create(sku_in)
    return sku
