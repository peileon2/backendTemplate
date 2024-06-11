from typing import List
from app.controller.sku_controllers import sku_controller
from app.schemas.sku_schema import SkuBase, SkuCreate, SkuUpdate
from fastapi import APIRouter, Query, HTTPException, status
from typing import Any

router = APIRouter()


# 根据id获取sku
@router.get("/{id}", response_model=SkuBase)
async def get_sku_by_id(id: int) -> Any:
    return await sku_controller.get(id=id)


@router.post("/", response_model=SkuCreate)
async def create_sku(sku_in: SkuCreate) -> Any:
    sku = await sku_controller.create(obj_in=sku_in)
    return sku


@router.post("/update", response_model=SkuUpdate)
async def update_sku(
    sku_in: SkuUpdate,
) -> Any:
    return await sku_controller.update(id=sku_in.id, obj_in=sku_in)


@router.delete("/delete", summary="删除")
async def delete_menu(
    id: int = Query(...),
):
    # child_menu_count = await sku_controller.model.filter(parent_id=id).count()
    # if child_menu_count > 0:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Cannot delete a menu with child menus",
    #     )
    await sku_controller.remove(id=id)
    return {"message": "Deleted Success"}
