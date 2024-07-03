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
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base, Query
from sqlalchemy.orm.attributes import InstrumentedAttribute
from pydantic import BaseModel
import logging
from uuid import UUID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

Total = NewType("Total", int)
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


## 根据id进行增删改查的基类
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession, user_id: str):
        self.model = model
        self.session = session
        self.user_id = str(user_id)  # Add user_id attribute

    async def get(self, id: int) -> Optional[ModelType]:
        try:
            query = select(self.model).filter_by(id=id, user_id=self.user_id)
            result = await self.session.execute(query)
            return result.scalar()
        except Exception as e:
            logger.error(f"Error fetching object with id {id}: {e}")
            return None

    async def get_list(
        self,
        page: int,
        page_size: int,
        order: Optional[List[InstrumentedAttribute]] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Total, List[ModelType]]:
        try:
            query = select(self.model).filter_by(user_id=self.user_id)
            if filters:
                for attr, value in filters.items():
                    query = query.filter(getattr(self.model, attr) == value)

            if order:
                query = query.order_by(*order)
            else:
                query = query.order_by(desc(self.model.id))

            total_count_query = select(func.count()).select_from(query.subquery())
            total_count_result = await self.session.execute(total_count_query)
            total_count_value = total_count_result.scalar() or 0

            paginated_query = query.offset((page - 1) * page_size).limit(page_size)
            result = await self.session.execute(paginated_query)
            items = list(result.scalars())  # 将 Sequence 转换为 List

            return Total(total_count_value), items
        except Exception as e:
            logger.error(f"Error fetching objects: {e}")
            return Total(0), []

    async def create(self, obj_in: CreateSchemaType) -> Optional[ModelType]:
        try:
            obj_in_data = obj_in.model_dump()
            obj_in_data["user_id"] = self.user_id  # Set user_id in the data
            obj = self.model(**obj_in_data)
            print(obj)
            self.session.add(obj)
            await self.session.commit()
            await self.session.refresh(obj)
            return obj
        except Exception as e:
            logger.error(f"Error creating object: {e}")
            await self.session.rollback()
            return None

    async def update(
        self, id: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> Optional[ModelType]:
        try:
            obj = await self.get(id)
            if obj is None:
                return None

            update_data = (
                obj_in.model_dump(exclude_unset=True)
                if isinstance(obj_in, BaseModel)
                else obj_in
            )
            # Ensure user_id is not updated
            if "user_id" in update_data:
                del update_data["user_id"]

            for key, value in update_data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)

            await self.session.commit()
            await self.session.refresh(obj)
            return obj
        except Exception as e:
            logger.error(f"Error updating object with id {id}: {e}")
            await self.session.rollback()
            return None

    async def remove(self, id: int) -> bool:
        try:
            obj = await self.get(id)
            if obj and obj.user_id == self.user_id:
                await self.session.delete(obj)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Error removing object with id {id}: {e}")
            await self.session.rollback()
            return False
