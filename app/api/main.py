from fastapi import APIRouter

from app.api.router import auth, fedex_deliveryFees, skus, users

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(skus.router, prefix="/sku", tags=["sku"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(
    fedex_deliveryFees.router, prefix="/aseemble", tags=["delivery"]
)
