from typing import Optional
from app.core.crud import CRUDBase
from app.models.sku import Sku
from app.schemas.sku_schema import SkuCreate, SkuUpdate


class SkuController(CRUDBase[Sku, SkuCreate, SkuUpdate]):
    def __init__(self):
        super().__init__(model=Sku)

    async def get_by_sku_name(self, name: str) -> Optional["Sku"]:
        return await self.model.filter(sku_name=name).first()


sku_controller = SkuController()
