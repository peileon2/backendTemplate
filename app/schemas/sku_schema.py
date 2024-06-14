from pydantic import BaseModel
from datetime import datetime


class SkuBase(BaseModel):
    sku_name: str
    height: float


class SkuCreate(BaseModel):
    sku_name: str
    height: float
    # create_time: datetime = datetime.now()


class SkuUpdate(BaseModel):
    id: int
    sku_name: str
    height: float
