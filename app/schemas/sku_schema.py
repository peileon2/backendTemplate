from pydantic import BaseModel
from datetime import datetime


class SkuBase(BaseModel):
    sku_name: str
    height: float
    length: float
    width: float
    weight: float


class SkuCreate(BaseModel):
    sku_name: str
    height: float
    length: float
    width: float
    weight: float


class SkuUpdate(BaseModel):
    id: int
    sku_name: str
    height: float
