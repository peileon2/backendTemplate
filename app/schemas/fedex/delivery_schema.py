from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

from app.schemas.ahs_schema import AhsCreate
from app.schemas.base_rate_schema import BaseRateCreate
from app.schemas.das_schema import DasCreate
from app.schemas.oversize_schema import OversizeCreate
from app.schemas.rdc_schema import RdcCreate


class AssembleDeliveryFeesBase(BaseModel):
    name: str


class AssembleDeliveryFeesCreate(AssembleDeliveryFeesBase):
    pass


class AssembleDeliveryFeesUpdate(AssembleDeliveryFeesBase):
    id: int


## CreateWithChidren
class AssembleDeliveryFeesChildren(AssembleDeliveryFeesBase):
    base_rates: List[BaseRateCreate] = []
    das_items: List[DasCreate] = []
    oversizes: List[OversizeCreate] = []
    ahs_items: List[AhsCreate] = []
    rdc_items: List[RdcCreate] = []

    class Config:
        orm_mode = True


class AssembleDeliveryFees(AssembleDeliveryFeesBase):
    id: int
    create_time: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True


class DemandChargeCreate:
    pass


class DemandChargeUpdate:
    pass
