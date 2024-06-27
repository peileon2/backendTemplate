from typing import Optional
from app.core.crud import CRUDBase
from app.models.sku import Sku
from app.schemas.sku_schema import SkuCreate, SkuUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SkuController(CRUDBase[Sku, SkuCreate, SkuUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Sku, session=session)

    async def get_by_sku_name(self, name: str) -> Optional[Sku]:
        try:
            result = await self.session.execute(
                select(self.model).filter_by(sku_name=name)
            )
            return result.scalar()
        except Exception as e:
            logger.error(f"Error fetching object with sku_name {name}: {e}")
            return None


# 在使用时，您需要提供一个AsyncSession实例
# sku_controller = SkuController(session=your_async_session)
