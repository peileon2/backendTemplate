from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Sku(Base):
    __tablename__ = "sku"

    sku_name = Column(String(50), nullable=False)
    height = Column(Float, nullable=False)
    create_time = Column(DateTime, server_default=func.now(), nullable=False)
