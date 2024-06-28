from typing import Optional
from app.core.crud import CRUDBase
from app.models.sku import Sku
from app.schemas.delivery_schema import (
    AssembleDeliveryFeesCreate,
    AssembleDeliveryFeesUpdate,
)
from app.models.deliverys import AssembleDeliveryFees, Ahs, BaseRate, Oversize, Das
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DeliveryController(
    CRUDBase[
        AssembleDeliveryFees, AssembleDeliveryFeesCreate, AssembleDeliveryFeesUpdate
    ]
):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Sku, session=session)
