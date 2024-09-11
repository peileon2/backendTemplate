from contextlib import asynccontextmanager

from fastapi import Depends, APIRouter

from app.api.db import User, create_db_and_tables
from app.schemas.user_schema import UserRead, UserUpdate
from fastapi import APIRouter, Query, HTTPException, status, Depends, Request
from app.api.deps import auth_backend, current_active_user, fastapi_users

router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    print(user.role)
    return {"message": f"Hello {user.email}!"}
