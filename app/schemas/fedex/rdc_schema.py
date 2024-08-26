from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import List
from app.models.Enums import GdAndHd, ResAndComm, AhsType, DasType


class RdcBase(BaseModel):
    name: str
    gd_hd_type: GdAndHd
    fees: float


class RdcCreate(RdcBase):
    pass


class RdcUpdate(RdcBase):
    id: int
    delivery_version_id: int


class Rdc(RdcBase):
    delivery_version_id: int
    create_time: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
