from contextlib import asynccontextmanager

from fastapi import Depends, APIRouter

from app.api.db import User, create_db_and_tables
from app.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.api.deps import auth_backend, current_active_user, fastapi_users


router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
