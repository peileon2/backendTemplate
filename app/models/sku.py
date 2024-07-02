from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func
from datetime import datetime


# 使用新的 DeclarativeBase
class Base(DeclarativeBase):
    pass


class Sku(Base):
    __tablename__ = "sku"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sku_name = Column(String(50), nullable=False, unique=True)
    height = Column(Float, nullable=False)
    length = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    user_id = Column(Integer, ForeignKey("user.id"))  # 添加外键字段
    # 使用 relationship 来定义与 User 表的关系
    user = relationship("User", back_populates="skus")
