import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import emails  # type: ignore
from jinja2 import Template
from jose import JWTError, jwt

from app.core.config import settings


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return str(decoded_token["sub"])
    except JWTError:
        return None
