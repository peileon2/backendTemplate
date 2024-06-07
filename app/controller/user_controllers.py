from typing import Optional
from app.core.crud import CRUDBase
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate


class UserController(CRUDBase[User, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(model=User)

    async def get_by_sku_name(self, name: str) -> Optional["User"]:
        return await self.model.filter(sku_name=name).first()


user_controller = UserController()
