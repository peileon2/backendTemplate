from typing import Optional, List, Type, Any
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
from app.schemas.delivery_schema import (
    AssembleDeliveryFeesCreate,
    AssembleDeliveryFeesUpdate,
    AssembleDeliveryFeesChildren,
    AhsCreate,
    AhsUpdate,
    OversizeCreate,
    OversizeUpdate,
    BaseRateCreate,
    BaseRateUpdate,
    DasCreate,
    DasUpdate,
    RdcCreate,
    RdcUpdate,
    DemandChargeCreate,
    DemandChargeUpdate,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AssembleController(
    CRUDBase[
        AssembleDeliveryFees, AssembleDeliveryFeesCreate, AssembleDeliveryFeesUpdate
    ]
):
    def __init__(self, session: AsyncSession, user_id: UUID):
        super().__init__(model=AssembleDeliveryFees, session=session, user_id=user_id)

    async def create_with_children(
        self, obj_in: AssembleDeliveryFeesChildren  # AssembleDeliveryFeesCreate,#
    ) -> AssembleDeliveryFees:
        try:
            new_assemble_delivery_fee = self.model(
                name=obj_in.name, user_id=self.user_id  # **obj_in.model_dump()
            )
            # 创建 BaseRate 子项
            for base_rate in obj_in.base_rates:
                new_base_rate = BaseRate(
                    name=base_rate.name,
                    delivery_version_id=new_assemble_delivery_fee.id,
                )
                new_assemble_delivery_fee.base_rates.append(new_base_rate)

            # 创建 Das 子项
            for das in obj_in.das_items:
                new_das = Das(
                    name=das.name, delivery_version_id=new_assemble_delivery_fee.id
                )
                new_assemble_delivery_fee.das_items.append(new_das)

            # 创建 Oversize 子项
            for oversize in obj_in.oversizes:
                new_oversize = Oversize(
                    name=oversize.name, delivery_version_id=new_assemble_delivery_fee.id
                )
                new_assemble_delivery_fee.oversizes.append(new_oversize)

            # 创建 Ahs 子项
            for ahs in obj_in.ahs_items:
                new_ahs = Ahs(
                    name=ahs.name, delivery_version_id=new_assemble_delivery_fee.id
                )
                new_assemble_delivery_fee.ahs_items.append(new_ahs)

            # 创建 Rdc 子项
            for rdc in obj_in.rdc_items:
                new_rdc = Rdc(
                    name=rdc.name, delivery_version_id=new_assemble_delivery_fee.id
                )
                new_assemble_delivery_fee.rdc_items.append(new_rdc)
            self.session.add(new_assemble_delivery_fee)  # 添加父对象到 session
            await self.session.commit()

            # 刷新并返回结果
            await self.session.refresh(new_assemble_delivery_fee)
            return new_assemble_delivery_fee
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error creating AssembleDeliveryFees with children: {e}")
            raise

    async def update_with_children(
        self,
        obj_in: AssembleDeliveryFeesUpdate,
        ahs_list: Optional[List[AhsUpdate]] = None,
        base_rate_list: Optional[List[BaseRateUpdate]] = None,
        oversize_list: Optional[List[OversizeUpdate]] = None,
        das_list: Optional[List[DasUpdate]] = None,
        rdc_list: Optional[List[RdcUpdate]] = None,
    ) -> Optional[AssembleDeliveryFees]:
        try:
            db_obj = await self.session.get(self.model, obj_in.id)
            if not db_obj:
                logger.error(f"Object with id {obj_in.id} not found.")
                return None

            for field, value in obj_in.dict(exclude_unset=True).items():
                setattr(db_obj, field, value)

            await self._update_children(
                ahs_list, base_rate_list, oversize_list, das_list, rdc_list
            )
            await self.session.commit()
            await self.session.refresh(db_obj)
            return db_obj
        except:
            await self.session.rollback()
            raise

    async def select_with_children(self, id: int) -> Optional[AssembleDeliveryFees]:
        try:
            result = await self.session.execute(
                select(self.model)
                .options(
                    joinedload(self.model.ahs_items),
                    joinedload(self.model.base_rates),
                    joinedload(self.model.oversizes),
                    joinedload(self.model.das_items),
                    joinedload(self.model.rdc_items),
                )
                .filter(self.model.id == id)
            )
            return result.scalars().first()
        except:
            await self.session.rollback()
            raise

    async def delete_with_children(self, id: int) -> bool:
        try:
            db_obj = await self.session.get(self.model, id)
            if not db_obj:
                logger.error(f"Object with id {id} not found.")
                return False

            await self.session.delete(db_obj)
            await self.session.commit()
            return True
        except:
            await self.session.rollback()

    async def _update_children(
        self,
        ahs_list: Optional[List[AhsUpdate]] = None,
        base_rate_list: Optional[List[BaseRateUpdate]] = None,
        oversize_list: Optional[List[OversizeUpdate]] = None,
        das_list: Optional[List[DasUpdate]] = None,
        rdc_list: Optional[List[RdcUpdate]] = None,
    ):
        if ahs_list:
            for ahs in ahs_list:
                ahs_obj = await self.session.get(Ahs, ahs.id)
                if ahs_obj:
                    for field, value in ahs.dict(exclude_unset=True).items():
                        setattr(ahs_obj, field, value)

        if base_rate_list:
            for base_rate in base_rate_list:
                base_rate_obj = await self.session.get(BaseRate, base_rate.id)
                if base_rate_obj:
                    for field, value in base_rate.dict(exclude_unset=True).items():
                        setattr(base_rate_obj, field, value)

        if oversize_list:
            for oversize in oversize_list:
                oversize_obj = await self.session.get(Oversize, oversize.id)
                if oversize_obj:
                    for field, value in oversize.dict(exclude_unset=True).items():
                        setattr(oversize_obj, field, value)

        if das_list:
            for das in das_list:
                das_obj = await self.session.get(Das, das.id)
                if das_obj:
                    for field, value in das.dict(exclude_unset=True).items():
                        setattr(das_obj, field, value)

        if rdc_list:
            for rdc in rdc_list:
                rdc_obj = await self.session.get(Rdc, rdc.id)
                if rdc_obj:
                    for field, value in rdc.dict(exclude_unset=True).items():
                        setattr(rdc_obj, field, value)


class BaseController(CRUDBase[BaseRate, BaseRateCreate, BaseRateUpdate]):
    def __init__(self, session: AsyncSession, user_id: UUID):
        super().__init__(model=BaseRate, session=session, user_id=user_id)

    async def get_fees_by_zone(self):
        try:
            query = select(self.model).filter_by(id=id, user_id=self.user_id)
            result = await self.session.execute(query)
            return result.scalar()
        except Exception as e:
            logger.error(f"Error fetching object with id {id}: {e}")
            return None


class AHSController(CRUDBase[Ahs, AhsCreate, AhsUpdate]):
    def __init__(self, session: AsyncSession, user_id: UUID):
        super().__init__(model=Ahs, session=session, user_id=user_id)


class OverSizeController(CRUDBase[Oversize, OversizeCreate, OversizeUpdate]):
    def __init__(self, session: AsyncSession, user_id: UUID):
        super().__init__(model=Oversize, session=session, user_id=user_id)


class DasController(CRUDBase[Das, DasCreate, DasUpdate]):
    def __init__(self, session: AsyncSession, user_id: UUID):
        super().__init__(model=Das, session=session, user_id=user_id)


class RdcController(CRUDBase[Rdc, RdcCreate, RdcUpdate]):
    def __init__(self, session: AsyncSession, user_id: UUID):
        super().__init__(model=Rdc, session=session, user_id=user_id)


class DemandChargeController(
    CRUDBase[DemandCharge, DemandChargeCreate, DemandChargeUpdate]
):
    def __init__(self, session: AsyncSession, user_id: UUID):
        super().__init__(model=Rdc, session=session, user_id=user_id)
