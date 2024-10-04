from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import List
from app.models.Enums import GdAndHd, ResAndComm, AhsType, DasType


class DasBase(BaseModel):
    das_type: DasType
    gd_hd_type: GdAndHd
    res_comm_type: ResAndComm
    fees: float


class DasCreate(DasBase):
    pass


class DasUpdate(DasBase):
    id: int


class Das(DasBase):
    id: int
    create_time: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
