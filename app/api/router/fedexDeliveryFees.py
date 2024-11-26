from fastapi import APIRouter, Query, HTTPException, status, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.db import get_async_session
from app.api.deps import current_active_user
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.models.user import User
from app.schemas.fedex.delivery_schema import (
    AssembleDeliveryFees,
    AssembleDeliveryFeesChildren,
    AssembleDeliveryFeesUpdate,
)
from app.controller.deliveryControllers import (
    AssembleController,
)
from app.controller.skuControllers import SkuController
from app.schemas.fedex.accurate import Accurate
from app.factorys.fedexFactory import FedexFactory, Judge

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
    if not await assemble_controller.is_in_user(id=id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wrong id")
    assemble = await assemble_controller.select_with_children(id=id)
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
    # assemble_data  <class 'app.schemas.fedex.delivery_schema.AssembleDeliveryFeesChildren'>
    return assemble_data


# 根据id删除Assemble
@router.delete("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_assemble_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    assemble_controller = AssembleController(session=session, user_id=user.id)
    if not await assemble_controller.is_in_user(id=id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wrong id")
    assemble = await assemble_controller.select_with_children(id=id)

    if assemble is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assemble not found"
        )

    # 调用控制器的删除方法
    await assemble_controller.delete_with_children(id=id)
    return None  # 删除操作成功返回空


# 根据id更新Assemble
@router.put("/{id}/update", response_model=AssembleDeliveryFees)  #
async def update_assemble_by_id(
    id: int,
    assemble_update: AssembleDeliveryFeesUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    assemble_controller = AssembleController(session=session, user_id=user.id)
    if not await assemble_controller.is_in_user(id=id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wrong id")
    # 查找要更新的Assemble记录
    assemble = await assemble_controller.select_with_children(id=id)

    if assemble is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assemble not found"
        )

    # 调用控制器的更新方法
    Updated_assemble = await assemble_controller.update_with_children(
        obj_in=assemble_update, delivery_id=id
    )
    return Updated_assemble


# 根据id获取Assemble,并算出fedex价格
@router.post("/accurate", response_model=AssembleDeliveryFees)
async def accurate_fedex(
    id: int,
    sku_id: int,
    accurate: Accurate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
) -> AssembleDeliveryFees:  ## 此处映射类存在问题
    assemble_controller = AssembleController(session=session, user_id=user.id)
    if not await assemble_controller.is_in_user(id=id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wrong id")
    ## 不要查主从表，直接通过accurate查子表，收入factory得出结论
    ## 先测试各个代码
    base_rate = assemble_controller.select_base_rate(id=id, filter_accurate=accurate)
    ahs = assemble_controller.select_base_rate(id=id, filter_accurate=accurate)
    os = assemble_controller.select_os(id=id, filter_accurate=accurate)
    rdc = assemble_controller.select_rdc(id=id, filter_accurate=accurate)
    das = assemble_controller.select_das(id=id, filter_accurate=accurate)
    demandsurchage = assemble_controller.select_demand_surcharge(id=id)
    ## 查出sku数据
    sku_controller = SkuController(session=session, user_id=user.id)
    if not await assemble_controller.is_in_user(id=id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wrong id")
    sku = SkuController.get(id=sku_id)
    Factory = FedexFactory(
        _sku=sku,
        _baserate=base_rate,
        _ahs=ahs,
        _das=das,
        _oversize=os,
        _rdc=rdc,
        _demandCharge=demandsurchage,
    )
    ##这里有问题factory需要根据judge的内容去修改
    ## 根据factory内容，算出Fedex报价类
