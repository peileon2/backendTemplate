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


## 内部采用user-id创建，外键id自动生成
class AhsCreate(AhsBase):
    pass


## 内部采用user-id修改，此处为主键id，外键delivery-id由router传入
class AhsUpdate(AhsBase):
    id: int


## 展示用类
class Ahs(AhsBase):
    create_time: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
