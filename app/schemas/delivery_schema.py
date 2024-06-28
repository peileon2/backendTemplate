from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


# BaseRate Pydantic 模型
class BaseRateBase(BaseModel):
    create_time: datetime
    rate_weight: int
    zone: int
    fees: float
    delivery_version_id: int


class BaseRateCreate(BaseRateBase):
    pass


class BaseRateUpdate(BaseRateBase):
    id: int


class BaseRateInDB(BaseRateBase):
    id: int

    class Config:
        orm_mode = True


# Das Pydantic 模型
class DasBase(BaseModel):
    create_time: datetime
    das_type: str
    gd_hd_type: str
    res_comm_type: str
    delivery_version_id: int


class DasCreate(DasBase):
    pass


class DasUpdate(DasBase):
    id: int


class DasInDB(DasBase):
    id: int
    delivery_version_id: int

    class Config:
        orm_mode = True


# Oversize Pydantic 模型
class OversizeBase(BaseModel):
    create_time: datetime
    os_type: str
    gd_hd_type: str
    fees: float
    delivery_version_id: int


class OversizeCreate(OversizeBase):
    pass


class OversizeUpdate(OversizeBase):
    id: int


class OversizeInDB(OversizeBase):
    id: int
    delivery_version_id: int

    class Config:
        orm_mode = True


# Ahs Pydantic 模型
class AhsBase(BaseModel):
    create_time: datetime
    ahs_type: str
    gd_hd_type: str
    res_comm_type: str
    delivery_version_id: int


class AhsCreate(AhsBase):
    pass


class AhsUpdate(AhsBase):
    id: int


class AhsInDB(AhsBase):
    id: int
    delivery_version_id: int

    class Config:
        orm_mode = True


# AssembleDeliveryFees Pydantic 模型
class AssembleDeliveryFeesBase(BaseModel):
    secoend_name: str
    create_time: datetime


class AssembleDeliveryFeesCreate(AssembleDeliveryFeesBase):
    pass


class AssembleDeliveryFeesUpdate(AssembleDeliveryFeesBase):
    id: int


class AssembleDeliveryFeesInDB(AssembleDeliveryFeesBase):
    id: int
    base_rates: List[BaseRateInDB] = []
    das_items: List[DasInDB] = []
    oversize_items: List[OversizeInDB] = []
    ahs_items: List[AhsInDB] = []

    class Config:
        orm_mode = True
