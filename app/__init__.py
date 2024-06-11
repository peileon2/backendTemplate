from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.api.main import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.VERSION,
)

register_tortoise(
    app,
    config=settings.TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
app.include_router(api_router, prefix=settings.API_V1_STR)
