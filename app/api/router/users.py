from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app.controller.user_controllers import user_controller
from app.api.deps import (
    CurrentUser,
    get_current_active_superuser,
)
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.utils import generate_new_account_email, send_email
from app.schemas.user_schema import UserCreate, UserBase

router = APIRouter()


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=UserBase
)
async def create_user(user_in: UserCreate) -> Any:
    """
    Create new user.
    """
    user = await user_controller.get_user_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    user = await user_controller.create_user(user_create=user_in)
    if settings.emails_enabled and user_in.email:
        email_data = generate_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
        send_email(
            email_to=user_in.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return user


@router.get("/{user_id}", response_model=UserBase)
def read_user_by_id(user_id: int, current_user: CurrentUser) -> Any:
    """
    Get a specific user by id.
    """
    user = user_controller.get(user_id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges",
        )
    return user
