from typing import Optional
from app.core.crud import CRUDBase
from app.models.sku import Sku
from app.models.deliverys import AssembleDeliveryFees, Ahs, BaseRate, Oversize, Das
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
    Rdc,
    RdcBase,
    RdcCreate,
    RdcUpdate
)
from app.models.deliverys import AssembleDeliveryFees, Ahs, BaseRate, Oversize, Das
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging
from uuid import UUID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AssembleController(
    CRUDBase[
        AssembleDeliveryFees, AssembleDeliveryFeesCreate, AssembleDeliveryFeesUpdate
    ]
):
    def __init__(self, session: AsyncSession, user_id: UUID):
        super().__init__(model=AssembleDeliveryFees, session=session, user_id=user_id)


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