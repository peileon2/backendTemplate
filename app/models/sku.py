from sqlalchemy import Column, String, Float, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
from datetime import datetime

# 使用新的 DeclarativeBase


class Base(DeclarativeBase):
    pass


class Sku(Base):
    __tablename__ = "sku"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sku_name = Column(String(50), nullable=False)
    height = Column(Float, nullable=False)
    create_time = Column(DateTime, nullable=False, server_default=func.now())
