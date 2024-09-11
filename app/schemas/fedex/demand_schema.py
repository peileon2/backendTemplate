from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import List


class DemandChargeBase(BaseModel):
    DIM: int
    peak_os_charge: float
    peak_rdc_charge: float
    fuel_rate: float


class DemandChargeCreate(DemandChargeBase):
    pass


class DemandChargeUpdate(DemandChargeBase):
    id: int


class DemandCharge(DemandChargeBase):
    create_time: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
