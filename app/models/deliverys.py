from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    Integer,
    ForeignKey,
    Enum as SqlEnum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.user import Base, User
from app.models.Enums import GdAndHd, ResAndComm, AhsType, DasType


class AssembleDeliveryFees(Base):
    __tablename__ = "assemble_delivery_fees"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    second_name = Column(String(50), nullable=False)
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    user_id = Column(String(36), ForeignKey(User.id))
    # 定义与 User 表的关系
    user = relationship("User", back_populates="assembleDeliveryFees")
    base_rates = relationship("BaseRate", back_populates="delivery_version", cascade="")
    # 一对多表
    das_items = relationship("Das", back_populates="delivery_version", cascade="")
    oversizes = relationship("Oversize", back_populates="delivery_version", cascade="")
    ahs_items = relationship("Ahs", back_populates="delivery_version", cascade="")
    rdc_items = relationship("Rdc", back_populates="delivery_version", cascade="")


class BaseRate(Base):
    __tablename__ = "base_rate"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    rate_weight = Column(Integer, nullable=False)
    zone = Column(Integer, nullable=False)
    fees = Column(Float, nullable=False)
    delivery_version_id = Column(Integer, ForeignKey(AssembleDeliveryFees.id))
    delivery_version = relationship("AssembleDeliveryFees", back_populates="base_rates")


class Das(Base):
    __tablename__ = "das"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    das_type = Column(SqlEnum(DasType), nullable=False)
    gd_hd_type = Column(SqlEnum(GdAndHd), nullable=False)
    res_comm_type = Column(SqlEnum(ResAndComm), nullable=False)
    fees = Column(Float, nullable=False)
    delivery_version_id = Column(Integer, ForeignKey(AssembleDeliveryFees.id))
    delivery_version = relationship("AssembleDeliveryFees", back_populates="das_items")


class Oversize(Base):
    __tablename__ = "oversize"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    gd_hd_type = Column(SqlEnum(GdAndHd), nullable=False)
    fees = Column(Float, nullable=False)
    delivery_version_id = Column(Integer, ForeignKey(AssembleDeliveryFees.id))
    delivery_version = relationship("AssembleDeliveryFees", back_populates="oversizes")


class Ahs(Base):
    __tablename__ = "ahs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    ahs_type = Column(SqlEnum(AhsType), nullable=False)
    gd_hd_type = Column(SqlEnum(GdAndHd), nullable=False)
    res_comm_type = Column(SqlEnum(ResAndComm), nullable=False)
    fees = Column(Float, nullable=False)
    delivery_version_id = Column(Integer, ForeignKey(AssembleDeliveryFees.id))
    delivery_version = relationship("AssembleDeliveryFees", back_populates="ahs_items")


class Rdc(Base):
    __tablename__ = "rdc"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    gd_hd_type = Column(SqlEnum(GdAndHd), nullable=False)
    fees = Column(Float, nullable=False)
    delivery_version_id = Column(Integer, ForeignKey(AssembleDeliveryFees.id))
    delivery_version = relationship("AssembleDeliveryFees", back_populates="rdc_items")
