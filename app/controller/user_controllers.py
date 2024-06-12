from typing import Optional
from tortoise.transactions import atomic
from app.core.crud import CRUDBase
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.core.security import verify_password
from app.core.security import get_password_hash


class UserController(CRUDBase[User, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(model=User)

    async def get_user_by_email(self, email: str) -> User | None:
        user = await User.get_or_none(email=email)
        return user

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        db_user = await self.get_user_by_email(email=email)
        if not db_user:
            return None
        if not verify_password(password, db_user.hashed_password):
            return None
        return db_user

    @atomic()
    async def create_user(self, user_create: UserCreate) -> User:
        db_obj = User(
            email=user_create.email,
            hashed_password=get_password_hash(user_create.password),
        )
        await db_obj.save()
        return db_obj


user_controller = UserController()
