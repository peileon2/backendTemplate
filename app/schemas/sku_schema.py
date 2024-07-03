from pydantic import BaseModel, ValidationError, field_validator
from datetime import datetime
from uuid import UUID


class SkuBase(BaseModel):
    sku_name: str
    height: float
    length: float
    width: float
    weight: float

    class Config:
        orm_mode = True


class SkuCreate(BaseModel):
    sku_name: str
    height: float
    length: float
    width: float
    weight: float
    user_id: str

    @field_validator("sku_name")
    def sku_name_must_be_unique(cls, v):
        # 自定义验证逻辑示例：检查 SKU 名称是否唯一
        if len(v) < 3:
            raise ValueError("SKU name must be at least 3 characters long")
        return v


class SkuUpdate(BaseModel):
    id: int
    sku_name: str
    height: float
    length: float
    width: float
    weight: float
    user_id: str
