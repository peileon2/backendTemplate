from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload, selectinload, aliased
from sqlalchemy.exc import NoResultFound
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
from app.schemas.fedex.accurate import Accurate

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

    async def is_in_user(self, id: int):
        # 假设这里是查询assemble的逻辑，并且检查是否属于当前用户
        assemble = await self.session.get(self.model, id)
        if assemble is None or assemble.user_id != self.user_id:
            return False  # 不存在或不属于该用户
        return True

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

    async def select_with_children(self, id: int) -> Optional[AssembleDeliveryFees]:
        """通过ID查询AssembleDeliveryFees对象及其子项"""
        try:
            result = await self.session.execute(
                select(self.model)
                .options(
                    joinedload(self.model.ahs_items),
                    # joinedload(self.model.base_rates),
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

    async def update_with_children(
        self, obj_in: AssembleDeliveryFeesUpdate, delivery_id: int
    ) -> AssembleDeliveryFees:
        try:
            db_obj = await self.session.get(self.model, delivery_id)
            if not db_obj:
                raise ValueError(f"Object with id {delivery_id} not found")

            # 更新父对象属性
            update_data = obj_in.model_dump(
                exclude_unset=True,
                exclude={
                    "das_items",
                    "oversizes",
                    "ahs_items",
                    "rdc_items",
                    "demand_item",
                },
            )
            for field, value in update_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)

            # 删除现有的子项
            await self.session.execute(
                delete(Ahs).where(Ahs.delivery_version_id == delivery_id)
            )
            await self.session.execute(
                delete(Das).where(Das.delivery_version_id == delivery_id)
            )
            await self.session.execute(
                delete(Oversize).where(Oversize.delivery_version_id == delivery_id)
            )
            await self.session.execute(
                delete(DemandCharge).where(
                    DemandCharge.delivery_version_id == delivery_id
                )
            )
            await self.session.execute(
                delete(Rdc).where(Rdc.delivery_version_id == delivery_id)
            )

            # 重新添加子项
            db_obj.das_items = [Das(**das.model_dump()) for das in obj_in.das_items]
            db_obj.oversizes = [
                Oversize(**oversize.model_dump()) for oversize in obj_in.oversizes
            ]
            db_obj.ahs_items = [Ahs(**ahs.model_dump()) for ahs in obj_in.ahs_items]
            db_obj.rdc_items = [Rdc(**rdc.model_dump()) for rdc in obj_in.rdc_items]

            # 创建 DemandCharge 子项
            if obj_in.demand_item:
                demand_charge_data = obj_in.demand_item.model_dump()
                db_obj.demand_charge = DemandCharge(**demand_charge_data)

            # 提交更新并刷新对象
            await self.session.commit()
            await self.session.refresh(db_obj)
            return db_obj  # 返回更新后的对象

        except Exception as e:
            logger.error(
                f"Error update AssembleDeliveryFees with id {delivery_id}: {e}"
            )
            await self.session.rollback()
            raise e  # 抛出异常或返回详细的错误信息

    async def select_base_rate(
        self, id: int, filter_accurate: Accurate, rate_weight: int
    ):
        """通过ID查询base_rate，并根据条件筛选子项"""
        try:
            # ahs 的查询
            query = select(BaseRate).filter_by(
                delivery_version_id=id,
                zone=filter_accurate.zone,
                rate_weight=rate_weight,
            )  #
            result = await self.session.execute(query)
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Error select AssembleDeliveryFees with id {id}: {e}")
            await self.session.rollback()
            raise e  # 抛出异常或返回详细的错误信息

    async def select_ahs(self, id: int, filter_accurate: Accurate):
        """通过ID查询，并根据条件筛选子项"""
        try:
            # ahs 的查询
            query = select(Ahs).filter_by(
                delivery_version_id=id,
                ahs_type=filter_accurate.ahs_type,
                gd_hd_type=filter_accurate.gd_hd_type,
                res_comm_type=filter_accurate.res_comm_type,
            )  #
            result = await self.session.execute(query)
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Error select AssembleDeliveryFees with id {id}: {e}")
            await self.session.rollback()
            raise e  # 抛出异常或返回详细的错误信息

    async def select_das(self, id: int, filter_accurate: Accurate):
        """通过ID查询AssembleDeliveryFees对象及其子项，并根据条件筛选子项"""
        try:
            # ahs 的查询
            query = select(Das).filter_by(
                delivery_version_id=id,
                das_type=filter_accurate.das_type,
                gd_hd_type=filter_accurate.gd_hd_type,
                res_comm_type=filter_accurate.res_comm_type,
            )  #
            result = await self.session.execute(query)
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Error select AssembleDeliveryFees with id {id}: {e}")
            await self.session.rollback()
            raise e  # 抛出异常或返回详细的错误信息

    async def select_rdc(self, id: int, filter_accurate: Accurate):
        """通过ID查询AssembleDeliveryFees对象及其子项，并根据条件筛选子项"""
        try:
            # ahs 的查询
            query = select(Rdc).filter_by(
                delivery_version_id=id, gd_hd_type=filter_accurate.gd_hd_type
            )  #
            result = await self.session.execute(query)
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Error select AssembleDeliveryFees with id {id}: {e}")
            await self.session.rollback()
            raise e  # 抛出异常或返回详细的错误信息

    async def select_os(self, id: int, filter_accurate: Accurate):
        """通过ID查询AssembleDeliveryFees对象及其子项，并根据条件筛选子项"""
        try:
            # ahs 的查询
            query = select(Oversize).filter_by(
                delivery_version_id=id, gd_hd_type=filter_accurate.gd_hd_type
            )  #
            result = await self.session.execute(query)
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Error select AssembleDeliveryFees with id {id}: {e}")
            await self.session.rollback()
            raise e  # 抛出异常或返回详细的错误信息

    async def select_demand_surcharge(self, id: int, filter_accurate: Accurate):
        """通过ID查询AssembleDeliveryFees对象及其子项，并根据条件筛选子项"""
        try:
            # ahs 的查询
            query = select(DemandCharge).filter_by(delivery_version_id=id)  #
            result = await self.session.execute(query)
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Error select AssembleDeliveryFees with id {id}: {e}")
            await self.session.rollback()
            raise e  # 抛出异常或返回详细的错误信息
