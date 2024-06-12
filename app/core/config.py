import os
import typing
from pydantic_settings import BaseSettings
from pydantic import (
    AnyUrl,
    BeforeValidator,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
)


class Settings(BaseSettings):
    VERSION: str = "0.1.0"
    APP_TITLE: str = "Vue FastAPI Template"
    PROJECT_NAME: str = "Vue FastAPI Template"
    APP_DESCRIPTION: str = "Description"
    CORS_ORIGINS: typing.List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: typing.List = ["*"]
    CORS_ALLOW_HEADERS: typing.List = ["*"]
    ALGORITHM: str = "HS256"
    DEBUG: bool = True
    DB_URL: str = "mysql://root:123456@localhost:3306/paddletest"
    PROJECT_ROOT: str = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    )
    API_V1_STR: str = "/api/v1"
    BASE_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
    LOGS_ROOT: str = os.path.join(BASE_DIR, "app/logs")
    SECRET_KEY: str = "3488a63e1765035d386f05409663f55c83bfae3b3c61a932744b20ad14244dcf"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    TORTOISE_ORM: dict = {
        "connections": {
            "mysql": {
                "engine": "tortoise.backends.mysql",
                "credentials": {
                    "host": "localhost",
                    "port": 3306,
                    "user": "root",
                    "password": "123456",
                    "database": "paddletest",
                },
            }
        },
        "apps": {
            "models": {
                "models": ["app.models.sku", "app.models.user"],
                "default_connection": "mysql",
            },
        },
        "use_tz": False,
        "timezone": "Asia/Shanghai",
    }
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    SMTP_HOST: str | None = None
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None

    @computed_field  # type: ignore[misc]
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)


settings = Settings()
