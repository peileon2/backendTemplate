from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import List


class DemandChargeBase(BaseModel):
    name: str


class DemandChargeCreate(DemandChargeBase):
    pass


class DemandChargeUpdate(DemandChargeBase):
    id: int


class DemandCharge(DemandChargeBase):
    class Config:
        orm_mode = True
