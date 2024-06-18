from typing import List
from app.controller.sku_controllers import SkuController
from app.schemas.sku_schema import SkuBase, SkuCreate, SkuUpdate
from fastapi import APIRouter, Query, HTTPException, status, Depends
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.db import get_async_session


from app.models.sku import Sku
from sqlalchemy import select

router = APIRouter()


@router.get("/test", response_model=SkuBase)
async def test_session(session: AsyncSession = Depends(get_async_session)):
    try:
        # 执行一个简单的查询来测试连接，例如查询表中的第一条记录
        query = select(Sku).limit(1)
        result = await session.execute(query)
        record = result.scalars().first()

        if record:
            # 如果查询到了记录，说明连接成功
            return record  # 返回查询到的记录或相应的响应
        else:
            # 如果没有查询到记录，可能是表为空
            return {"message": "Database connection successful, but no records found."}
    except Exception as e:
        # 如果发生异常，说明连接失败
        return {"message": f"Database connection failed: {e}"}
    finally:
        # 关闭会话
        await session.close()


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
async def create_sku(sku: SkuCreate, session: AsyncSession = Depends(get_async_session)):
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
