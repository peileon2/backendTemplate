from pydantic import BaseModel


class Sku(BaseModel):
    sku_name: str
    height: float


class SkuCreate(BaseModel):
    sku_name: str
    height: float


class SkuUpdate(BaseModel):
    sku_name: str
    height: float
