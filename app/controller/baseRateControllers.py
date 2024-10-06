from typing import Optional, List, Dict, Tuple, Any
from app.models.deliverys import BaseRate
from app.schemas.fedex.base_rate_schema import BaseRateCreate, BaseRateUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import InstrumentedAttribute
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseRateController:
    def __init__(self, session: AsyncSession, delivery_id: int):
        """Initialize BaseRateController with session and delivery_id."""
        self.session = session
        self.delivery_id = delivery_id

    async def get(self, id: int) -> Optional[BaseRate]:
        """Retrieve a BaseRate by id and delivery_version_id."""
        try:
            query = select(BaseRate).filter_by(
                id=id, delivery_version_id=self.delivery_id
            )
            result = await self.session.execute(query)
            return result.scalar_one_or_none()  # Return the object or None
        except Exception as e:
            logger.error(f"Error fetching BaseRate with id {id}: {e}")
            return None

    async def get_list(
        self,
        page: int,
        page_size: int,
        order: Optional[List[InstrumentedAttribute]] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Tuple[int, List[BaseRate]]:
        """Retrieve a paginated list of BaseRate objects."""
        try:
            query = select(BaseRate).filter_by(delivery_version_id=self.delivery_id)

            # Apply filters if provided
            if filters:
                for attr, value in filters.items():
                    query = query.filter(getattr(BaseRate, attr) == value)

            # Apply ordering
            if order:
                query = query.order_by(*order)
            else:
                query = query.order_by(desc(BaseRate.id))

            # Get the total count of items
            total_count_query = select(func.count()).select_from(query.subquery())
            total_count_result = await self.session.execute(total_count_query)
            total_count = total_count_result.scalar() or 0

            # Apply pagination
            paginated_query = query.offset((page - 1) * page_size).limit(page_size)
            result = await self.session.execute(paginated_query)
            items = result.scalars().all()  # Retrieve all items as a list

            return total_count, items
        except Exception as e:
            logger.error(f"Error fetching BaseRate list: {e}")
            return 0, []

    async def create(self, obj_in: BaseRateCreate) -> Optional[BaseRate]:
        """Create a new BaseRate object."""
        try:
            obj_in_data = obj_in.model_dump()  # Convert Pydantic object to dict
            obj_in_data["delivery_version_id"] = (
                self.delivery_id
            )  # Set delivery_version_id
            obj = BaseRate(**obj_in_data)  # Create a new BaseRate object

            self.session.add(obj)
            await self.session.commit()
            await self.session.refresh(obj)
            return obj
        except Exception as e:
            logger.error(f"Error creating BaseRate: {e}")
            await self.session.rollback()
            return None

    async def update(self, id: int, obj_in: BaseRateUpdate) -> Optional[BaseRate]:
        """Update an existing BaseRate object."""
        try:
            obj = await self.get(id)  # Fetch the existing object
            if obj is None:
                return None

            update_data = obj_in.model_dump(
                exclude_unset=True
            )  # Only update fields that are set
            if "delivery_version_id" in update_data:
                del update_data[
                    "delivery_version_id"
                ]  # Prevent modification of delivery_version_id

            for key, value in update_data.items():
                setattr(obj, key, value)  # Set new values for the object

            await self.session.commit()
            await self.session.refresh(obj)
            return obj
        except Exception as e:
            logger.error(f"Error updating BaseRate with id {id}: {e}")
            await self.session.rollback()
            return None

    async def remove(self, id: int) -> bool:
        """Remove a BaseRate object by id."""
        try:
            obj = await self.get(id)
            if obj is None or obj.delivery_version_id != self.delivery_id:
                return False

            await self.session.delete(obj)
            await self.session.commit()
            return True
        except Exception as e:
            logger.error(f"Error removing BaseRate with id {id}: {e}")
            await self.session.rollback()
            return False
