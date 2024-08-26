from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import List
from app.models.Enums import GdAndHd, ResAndComm, AhsType, DasType


class AhsBase(BaseModel):
    name: str
    ahs_type: AhsType
    gd_hd_type: GdAndHd
    res_comm_type: ResAndComm
    fees: float


class AhsCreate(AhsBase):
    pass


class AhsUpdate(AhsBase):
    id: int


class Ahs(AhsBase):
    class Config:
        orm_mode = True
