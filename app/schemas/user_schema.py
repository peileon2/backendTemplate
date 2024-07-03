import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    role :str
    company :str


class UserUpdate(schemas.BaseUserUpdate):
    pass