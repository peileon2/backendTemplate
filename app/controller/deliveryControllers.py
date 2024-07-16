from typing import Optional, List, Type, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
import logging
from uuid import UUID

from app.core.crud import CRUDBase
from app.models.deliverys import AssembleDeliveryFees, Ahs, BaseRate, Oversize, Das, Rdc
from app.schemas.delivery_schema import (
    AssembleDeliveryFeesCreate,
    AssembleDeliveryFeesUpdate,
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
        self,
        obj_in: AssembleDeliveryFeesCreate,
        ahs_list: Optional[List[AhsCreate]] = None,
        base_rate_list: Optional[List[BaseRateCreate]] = None,
        oversize_list: Optional[List[OversizeCreate]] = None,
        das_list: Optional[List[DasCreate]] = None,
        rdc_list: Optional[List[RdcCreate]] = None,
    ) -> AssembleDeliveryFees:
        try:
            db_obj = self.model(**obj_in.dict(), user_id=self.user_id)
            self.session.add(db_obj)
            await self.session.flush()
            # 添加子对象
            await self._add_children(
                db_obj.id, ahs_list, base_rate_list, oversize_list, das_list, rdc_list
            )
            # 提交事务
            await self.session.commit()
            await self.session.refresh(db_obj)
            return db_obj
        except:
            # 如果有错误，回滚事务
            await self.session.rollback()

    async def update_with_children(
        self,
        obj_in: AssembleDeliveryFeesUpdate,
        ahs_list: Optional[List[AhsUpdate]] = None,
        base_rate_list: Optional[List[BaseRateUpdate]] = None,
        oversize_list: Optional[List[OversizeUpdate]] = None,
        das_list: Optional[List[DasUpdate]] = None,
        rdc_list: Optional[List[RdcUpdate]] = None,
    ) -> Optional[AssembleDeliveryFees]:
        async with self.session.begin():
            db_obj = await self.session.get(self.model, obj_in.id)
            if not db_obj:
                logger.error(f"Object with id {obj_in.id} not found.")
                return None

            for field, value in obj_in.dict(exclude_unset=True).items():
                setattr(db_obj, field, value)

            await self._update_children(
                ahs_list, base_rate_list, oversize_list, das_list, rdc_list
            )
            await self.session.refresh(db_obj)
            return db_obj

    async def select_with_children(self, id: int) -> Optional[AssembleDeliveryFees]:
        async with self.session() as session:
            result = await session.execute(
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

    async def delete_with_children(self, id: int) -> bool:
        async with self.session.begin():
            db_obj = await self.session.get(self.model, id)
            if not db_obj:
                logger.error(f"Object with id {id} not found.")
                return False

            await self.session.delete(db_obj)
            return True

    async def _add_children(
        self,
        parent_id: UUID,
        ahs_list: Optional[List[AhsCreate]] = None,
        base_rate_list: Optional[List[BaseRateCreate]] = None,
        oversize_list: Optional[List[OversizeCreate]] = None,
        das_list: Optional[List[DasCreate]] = None,
        rdc_list: Optional[List[RdcCreate]] = None,
    ):
        if ahs_list:
            for ahs in ahs_list:
                ahs_obj = Ahs(**ahs.dict(), delivery_version_id=parent_id)
                self.session.add(ahs_obj)
        if base_rate_list:
            for base_rate in base_rate_list:
                base_rate_obj = BaseRate(
                    **base_rate.dict(), delivery_version_id=parent_id
                )
                self.session.add(base_rate_obj)
        if oversize_list:
            for oversize in oversize_list:
                oversize_obj = Oversize(
                    **oversize.dict(), delivery_version_id=parent_id
                )
                self.session.add(oversize_obj)
        if das_list:
            for das in das_list:
                das_obj = Das(**das.dict(), delivery_version_id=parent_id)
                self.session.add(das_obj)
        if rdc_list:
            for rdc in rdc_list:
                rdc_obj = Rdc(**rdc.dict(), delivery_version_id=parent_id)
                self.session.add(rdc_obj)

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
