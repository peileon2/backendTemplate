from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.user import Base, User


class Sku(Base):
    __tablename__ = "sku"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sku_name = Column(String(50), nullable=False, unique=True)
    height = Column(Float, nullable=False)
    length = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    create_time = Column(DateTime, nullable=False)
    user_id = Column(String(36), ForeignKey(User.id))  # 使用 UUID 类型作为外键

    # 定义与 User 表的关系
    user = relationship("User", back_populates="skus")
