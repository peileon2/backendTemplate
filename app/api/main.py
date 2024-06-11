from fastapi import APIRouter

from app.api.router import skus, login, users

api_router = APIRouter()
# api_router.include_router(login.router, tags=["login"])
api_router.include_router(skus.router, prefix="/sku", tags=["sku"])
api_router.include_router(login.router, prefix="/sku", tags=["login"])
api_router.include_router(login.router, prefix="/users", tags=["users"])
