from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, String, Float, DateTime, Integer


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    role = Column(String(50), nullable=False)
    company = Column(String(50), nullable=False)
    # 定义与 Sku 表的关系
    skus = relationship("Sku", back_populates="user", cascade="")
    assembleDeliveryFees = relationship(
        "AssembleDeliveryFees", back_populates="user", cascade=""
    )
