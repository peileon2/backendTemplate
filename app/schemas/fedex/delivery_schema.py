from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

from app.schemas.fedex.ahs_schema import AhsCreate, Ahs, AhsUpdate
from app.schemas.fedex.base_rate_schema import BaseRateCreate, BaseRate, BaseRateUpdate
from app.schemas.fedex.das_schema import DasCreate, Das, DasUpdate
from app.schemas.fedex.oversize_schema import OversizeCreate, Oversize, OversizeUpdate
from app.schemas.fedex.rdc_schema import RdcCreate, Rdc, RdcUpdate
from app.schemas.fedex.demand_schema import (
    DemandChargeCreate,
    DemandCharge,
    DemandChargeUpdate,
)


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
class AssembleDeliveryFeesUpdate(BaseModel):
    name: str
    das_items: List[DasCreate] = []
    oversizes: List[OversizeCreate] = []
    ahs_items: List[AhsCreate] = []
    rdc_items: List[RdcCreate] = []
    demand_item: Optional[DemandChargeCreate]


## CreateWithChidren
class AssembleDeliveryFeesChildren(AssembleDeliveryFeesBase):
    pass


# 存在一对多关系
class AssembleDeliveryFees(BaseModel):
    id: int
    name: str
    create_time: datetime = Field(default_factory=datetime.utcnow)
    # base_rates: List[BaseRate] = []
    das_items: List[Das] = []
    oversizes: List[Oversize] = []
    ahs_items: List[Ahs] = []
    rdc_items: List[Rdc] = []
    demand_charge: Optional[DemandCharge] = None

    class Config:
        from_attributes = True


# class AssembleDeliveryFees(BaseModel):
#     id: int
#     name: str
#     create_time: datetime = Field(default_factory=datetime.utcnow)
#     base_rates: List[BaseRate] = []
#     das_items: List[Das] = []
#     oversizes: List[Oversize] = []
#     ahs_items: List[Ahs] = []
#     rdc_items: List[Rdc] = []
#     demand_charge: Optional[DemandCharge] = None

#     class Config:
#         from_attributes = True
