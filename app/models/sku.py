from sqlalchemy import Column, String, Float, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class Sku(Base):
    __tablename__ = "sku"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sku_name = Column(String(50), nullable=False)
    height = Column(Float, nullable=False)
    create_time = Column(DateTime, nullable=False, default=datetime.now())
