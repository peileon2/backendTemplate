from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import List
from app.models.Enums import GdAndHd, ResAndComm, AhsType, DasType


class BaseRateBase(BaseModel):
    name: str

    # rate_weight: int
    # zone: int
    # fees: float


class BaseRateCreate(BaseRateBase):
    pass



class BaseRateUpdate(BaseRateBase):
    id: int
    delivery_version_id: int


class BaseRate(BaseRateBase):
    id: int
    delivery_version_id: int
    create_time: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True


class DasBase(BaseModel):
    name: str

    # das_type: DasType
    # gd_hd_type: GdAndHd
    # res_comm_type: ResAndComm
    # fees: float


class DasCreate(DasBase):
    pass


class DasUpdate(DasBase):
    id: int
    delivery_version_id: int


class Das(DasBase):
    id: int
    delivery_version_id: int
    create_time: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True


class OversizeBase(BaseModel):
    name: str
    # gd_hd_type: GdAndHd
    # fees: float


class OversizeCreate(OversizeBase):
    pass


class OversizeUpdate(OversizeBase):
    id: int



class Oversize(OversizeBase):
    id: int
    delivery_version_id: int
    create_time: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True


class AhsBase(BaseModel):
    name: str
    # ahs_type: AhsType
    # gd_hd_type: GdAndHd
    # res_comm_type: ResAndComm
    # fees: float



class AhsCreate(AhsBase):
    pass


class AhsUpdate(AhsBase):
    id: int


class Ahs(AhsBase):
    class Config:
        orm_mode = True


class RdcBase(BaseModel):
    name: str
    # gd_hd_type: GdAndHd 
    # fees: float


class RdcCreate(RdcBase):
    pass

class RdcUpdate(RdcBase):
    id: int
    delivery_version_id: int


class Rdc(RdcBase):
    id: int
    delivery_version_id: int
    create_time: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True


class AssembleDeliveryFeesBase(BaseModel):
    name: str


class AssembleDeliveryFeesCreate(AssembleDeliveryFeesBase):
    pass


class AssembleDeliveryFeesUpdate(AssembleDeliveryFeesBase):
    id: int


class AssembleDeliveryFeesChildren(AssembleDeliveryFeesBase):
    id: int
    base_rates: List[BaseRate] = []
    das_items: List[Das] = []
    oversizes: List[Oversize] = []
    ahs_items: List[Ahs] = []
    rdc_items: List[Rdc] = []

    class Config:
        orm_mode = True


class AssembleDeliveryFees(AssembleDeliveryFeesBase):
    id: int
    create_time: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
