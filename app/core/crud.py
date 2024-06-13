from typing import Any, Dict, Generic, List, NewType, Tuple, Type, TypeVar, Union
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.expression import ClauseElement

Base = declarative_base()

Total = NewType("Total", int)
ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: int) -> ModelType:
        return await self.session.execute(select(self.model).filter_by(id=id)).scalar()

    async def get_list(
        self,
        page: int,
        page_size: int,
        search: ClauseElement = None,
        order: list = None,
    ) -> Tuple[Total, List[ModelType]]:
        query = select(self.model)
        if search is not None:
            query = query.filter(search)
        total_count = await self.session.execute(query.count()).scalar()
        query = query.offset((page - 1) * page_size).limit(page_size)
        if order is not None:
            query = query.order_by(*order)
        item_lists = await self.session.execute(query).scalars().all()
        return (total_count, item_lists)

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj = self.model(**obj_in.dict())
        self.session.add(obj)
        await self.session.commit()
        return obj

    async def update(
        self, id: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj = await self.get(id)
        for key, value in obj_in.dict(exclude_unset=True).items():
            setattr(obj, key, value)
        await self.session.commit()
        return obj

    async def remove(self, id: int) -> None:
        obj = await self.get(id)
        self.session.delete(obj)
        await self.session.commit()
