from pydantic import BaseModel


class SkuBase(BaseModel):
    sku_name: str
    height: float


class SkuCreate(BaseModel):
    sku_name: str
    height: float


class SkuUpdate(BaseModel):
    id: int
    sku_name: str
    height: float
