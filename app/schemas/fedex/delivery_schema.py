from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

from app.schemas.fedex.ahs_schema import AhsCreate
from app.schemas.fedex.base_rate_schema import BaseRateCreate
from app.schemas.fedex.das_schema import DasCreate
from app.schemas.fedex.oversize_schema import OversizeCreate
from app.schemas.fedex.rdc_schema import RdcCreate
from app.schemas.fedex.demand_schema import DemandChargeCreate


class AssembleDeliveryFeesBase(BaseModel):
    name: str


# class AssembleDeliveryFeesCreate(AssembleDeliveryFeesBase):
#     pass


## 根据主键修改
class AssembleDeliveryFeesUpdate(AssembleDeliveryFeesBase):
    id: int


## CreateWithChidren
class AssembleDeliveryFeesChildren(AssembleDeliveryFeesBase):
    base_rates: List[BaseRateCreate] = []
    das_items: List[DasCreate] = []
    oversizes: List[OversizeCreate] = []
    ahs_items: List[AhsCreate] = []
    rdc_items: List[RdcCreate] = []
    demand_item: DemandChargeCreate

    class Config:
        orm_mode = True


class AssembleDeliveryFees(AssembleDeliveryFeesBase):
    id: int
    create_time: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
