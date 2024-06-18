from fastapi import APIRouter

from app.api.router import skus,users

api_router = APIRouter()
api_router.include_router(users.router,prefix="/auth", tags=["auth"])
api_router.include_router(skus.router, prefix="/sku", tags=["sku"])
