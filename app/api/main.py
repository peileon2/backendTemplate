from fastapi import APIRouter

from app.api.router import skus

api_router = APIRouter()
# api_router.include_router(login.router, tags=["login"])
api_router.include_router(skus.router, prefix="/sku", tags=["users"])
