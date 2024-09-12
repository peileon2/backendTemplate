from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
import logging
from uuid import UUID

from app.core.crud import CRUDBase
from app.models.deliverys import (
    AssembleDeliveryFees,
    Ahs,
    BaseRate,
    Oversize,
    Das,
    Rdc,
    DemandCharge,
)
from app.schemas.fedex.delivery_schema import (
    AssembleDeliveryFeesUpdate,
    AssembleDeliveryFeesChildren,
)

# from app.schemas.fedex.ahs_schema import AhsUpdate
# from app.schemas.fedex.base_rate_schema import BaseRateUpdate
# from app.schemas.fedex.das_schema import DasUpdate
# from app.schemas.fedex.oversize_schema import OversizeUpdate
# from app.schemas.fedex.rdc_schema import RdcUpdate
# from app.schemas.fedex.demand_schema import DemandChargeUpdate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AssembleController(
    CRUDBase[
        AssembleDeliveryFees, AssembleDeliveryFeesChildren, AssembleDeliveryFeesUpdate
    ]
):
    def __init__(self, session: AsyncSession, user_id: UUID):
        super().__init__(model=AssembleDeliveryFees, session=session, user_id=user_id)

    async def create_with_children(
        self, obj_in: AssembleDeliveryFeesChildren
    ) -> Optional[AssembleDeliveryFees]:
        """创建带有子项的AssembleDeliveryFees对象"""
        try:
            new_assemble_delivery_fee = self.model(
                name=obj_in.name, user_id=self.user_id
            )

            # 创建 BaseRate 子项
            for base_rate in obj_in.base_rates:
                base_rate_data = base_rate.model_dump()
                new_base_rate = BaseRate(**base_rate_data)
                new_assemble_delivery_fee.base_rates.append(new_base_rate)

            # 创建 Das 子项
            for das in obj_in.das_items:
                das_data = das.model_dump()
                new_das = Das(**das_data)
                new_assemble_delivery_fee.das_items.append(new_das)

            # 创建 Oversize 子项
            for oversize in obj_in.oversizes:
                oversize_data = oversize.model_dump()
                new_oversize = Oversize(**oversize_data)
                new_assemble_delivery_fee.oversizes.append(new_oversize)

            # 创建 Ahs 子项
            for ahs in obj_in.ahs_items:
                ahs_data = ahs.model_dump()
                new_ahs = Ahs(**ahs_data)
                new_assemble_delivery_fee.ahs_items.append(new_ahs)

            # 创建 Rdc 子项
            for rdc in obj_in.rdc_items:
                rdc_data = rdc.model_dump()
                new_rdc = Rdc(**rdc_data)
                new_assemble_delivery_fee.rdc_items.append(new_rdc)

            # 创建 DemandCharge 子项（如果有）
            if obj_in.demand_item:
                demand_charge_data = obj_in.demand_item.model_dump()
                new_assemble_delivery_fee.demand_charge = DemandCharge(
                    **demand_charge_data
                )

            self.session.add(new_assemble_delivery_fee)  # 添加父对象到 session
            await self.session.commit()

            # 刷新并返回结果
            await self.session.refresh(new_assemble_delivery_fee)
            return new_assemble_delivery_fee
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error creating AssembleDeliveryFees with children: {e}")
            return None

    async def update_with_children(
        self, obj_in: AssembleDeliveryFeesUpdate
    ) -> Optional[AssembleDeliveryFees]:
        """更新带有子项的AssembleDeliveryFees对象"""
        try:
            db_obj = await self.session.get(self.model, obj_in.id)
            if not db_obj:
                logger.error(f"Object with id {obj_in.id} not found.")
                return None

            # 更新父对象的字段
            for field, value in obj_in.dict(exclude_unset=True).items():
                setattr(db_obj, field, value)

            # 更新子项
            await self._update_children(obj_in)
            await self.session.commit()
            await self.session.refresh(db_obj)
            return db_obj
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error updating AssembleDeliveryFees with children: {e}")
            return None

    async def select_with_children(self, id: int) -> Optional[AssembleDeliveryFees]:
        """通过ID查询AssembleDeliveryFees对象及其子项"""
        try:
            result = await self.session.execute(
                select(self.model)
                .options(
                    joinedload(self.model.ahs_items),
                    joinedload(self.model.base_rates),
                    joinedload(self.model.oversizes),
                    joinedload(self.model.das_items),
                    joinedload(self.model.rdc_items),
                    joinedload(self.model.demand_charge),
                )
                .filter(self.model.id == id)
            )
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Error selecting AssembleDeliveryFees with id {id}: {e}")
            await self.session.rollback()
            return None

    async def delete_with_children(self, id: int) -> bool:
        """删除带有子项的AssembleDeliveryFees对象"""
        try:
            db_obj = await self.session.get(self.model, id)
            if not db_obj:
                logger.error(f"Object with id {id} not found.")
                return False

            await self.session.delete(db_obj)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error deleting AssembleDeliveryFees with id {id}: {e}")
            return False

    async def _update_children(self, obj_in: AssembleDeliveryFeesUpdate):
        """私有方法，更新多个子项"""

        async def update_child(child_obj, update_data):
            """更新子项的通用方法"""
            for field, value in update_data.dict(exclude_unset=True).items():
                setattr(child_obj, field, value)

        # 更新 Ahs 子项
        if obj_in.ahs_items:
            for ahs in obj_in.ahs_items:
                ahs_obj = await self.session.get(Ahs, ahs.id)
                if ahs_obj:
                    await update_child(ahs_obj, ahs)

        # 更新 BaseRate 子项
        if obj_in.base_rates:
            for base_rate in obj_in.base_rates:
                base_rate_obj = await self.session.get(BaseRate, base_rate.id)
                if base_rate_obj:
                    await update_child(base_rate_obj, base_rate)

        # 更新 Oversize 子项
        if obj_in.oversizes:
            for oversize in obj_in.oversizes:
                oversize_obj = await self.session.get(Oversize, oversize.id)
                if oversize_obj:
                    await update_child(oversize_obj, oversize)

        # 更新 Das 子项
        if obj_in.das_items:
            for das in obj_in.das_items:
                das_obj = await self.session.get(Das, das.id)
                if das_obj:
                    await update_child(das_obj, das)

        # 更新 Rdc 子项
        if obj_in.rdc_items:
            for rdc in obj_in.rdc_items:
                rdc_obj = await self.session.get(Rdc, rdc.id)
                if rdc_obj:
                    await update_child(rdc_obj, rdc)

        # 更新 DemandCharge 子项（如果有）
        if obj_in.demand_item:
            demand_obj = await self.session.get(DemandCharge, obj_in.demand_item.id)
            if demand_obj:
                await update_child(demand_obj, obj_in.demand_item)
