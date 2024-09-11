from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import List
from app.models.Enums import GdAndHd, ResAndComm, AhsType, DasType


class BaseRateBase(BaseModel):
    rate_weight: int
    zone: int
    fees: float


class BaseRateCreate(BaseRateBase):
    pass


class BaseRateUpdate(BaseRateBase):
    id: int


class BaseRate(BaseRateBase):
    create_time: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
