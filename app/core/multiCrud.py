## 根据外键批量增删改查
from typing import (
    Any,
    Dict,
    Generic,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    NewType,
)
from sqlalchemy import select, func, desc, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base, Query, DeclarativeBase
from sqlalchemy.orm.attributes import InstrumentedAttribute
from pydantic import BaseModel
import logging
from app.core.crud import CRUDBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Total = NewType("Total", int)
ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class MultiCRUDBase(CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        super().__init__(model, session)

    async def create_bulk(
        self, objs_in: List[CreateSchemaType]
    ) -> Optional[List[ModelType]]:
        try:
            objs_in_data = [obj_in.model_dump() for obj_in in objs_in]
            objs = [self.model(**obj_in_data) for obj_in_data in objs_in_data]
            self.session.add_all(objs)
            await self.session.commit()
            for obj in objs:
                await self.session.refresh(obj)
            return objs
        except Exception as e:
            logger.error(f"Error creating objects: {e}")
            await self.session.rollback()
            return None
