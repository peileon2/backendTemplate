from fastapi import APIRouter

from app.api.router import auth, skus, users, delivery_fees, Ahs_fees

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(skus.router, prefix="/sku", tags=["sku"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(delivery_fees.router, prefix="/aseemble", tags=["delivery"])
api_router.include_router(Ahs_fees.router, prefix="/ahs", tags=["Ahs_fees"])
