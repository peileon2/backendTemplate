from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

from app.schemas.fedex.ahs_schema import AhsCreate, Ahs
from app.schemas.fedex.base_rate_schema import BaseRateCreate, BaseRate
from app.schemas.fedex.das_schema import DasCreate, Das
from app.schemas.fedex.oversize_schema import OversizeCreate, Oversize
from app.schemas.fedex.rdc_schema import RdcCreate, Rdc
from app.schemas.fedex.demand_schema import DemandChargeCreate, DemandCharge


class AssembleDeliveryFeesBase(BaseModel):
    name: str
    base_rates: List[BaseRateCreate] = []
    das_items: List[DasCreate] = []
    oversizes: List[OversizeCreate] = []
    ahs_items: List[AhsCreate] = []
    rdc_items: List[RdcCreate] = []
    demand_item: Optional[DemandChargeCreate]


# class AssembleDeliveryFeesCreate(AssembleDeliveryFeesBase):
#     pass


## 根据主键修改
class AssembleDeliveryFeesUpdate(AssembleDeliveryFeesBase):
    id: int


## CreateWithChidren
class AssembleDeliveryFeesChildren(AssembleDeliveryFeesBase):
    pass


# 存在一对多关系
class AssembleDeliveryFees(BaseModel):
    name: str
    base_rates: List[BaseRate] = []
    das_items: List[Das] = []
    oversizes: List[Oversize] = []
    ahs_items: List[Ahs] = []
    rdc_items: List[Rdc] = []
    demand_item: Optional[DemandCharge] = None
    id: int
    create_time: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
