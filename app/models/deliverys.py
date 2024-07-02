from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    Integer,
    ForeignKey,
    Enum as SqlEnum,
)
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func
from enum import Enum


class GdAndHd(Enum):
    GROUND = 1
    HOMEDELIVERY = 2


class ResAndComm(Enum):
    RESIDENTIAL = 1
    COMMERCIAL = 2


class AhsType(Enum):
    AHS_Dimension = 1
    AHS_Weight = 2
    AHS_Packing = 3


class DasType(Enum):
    DAS = 1
    DASE = 2
    RAS = 3


class Base(DeclarativeBase):
    pass


class AssembleDeliveryFees(Base):
    __tablename__ = "assemble_delivery_fees"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    second_name = Column(String(50), nullable=False)
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    base_rates = relationship("BaseRate", back_populates="delivery_version", cascade="")
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
    delivery_version_id = Column(Integer, ForeignKey("assemble_delivery_fees.id"))
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
    delivery_version_id = Column(Integer, ForeignKey("assemble_delivery_fees.id"))
    delivery_version = relationship("AssembleDeliveryFees", back_populates="das_items")


class Oversize(Base):
    __tablename__ = "oversize"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    gd_hd_type = Column(SqlEnum(GdAndHd), nullable=False)
    fees = Column(Float, nullable=False)
    delivery_version_id = Column(Integer, ForeignKey("assemble_delivery_fees.id"))
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
    delivery_version_id = Column(Integer, ForeignKey("assemble_delivery_fees.id"))
    delivery_version = relationship("AssembleDeliveryFees", back_populates="ahs_items")


class Rdc(Base):
    __tablename__ = "rdc"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    gd_hd_type = Column(SqlEnum(GdAndHd), nullable=False)
    fees = Column(Float, nullable=False)
    delivery_version_id = Column(Integer, ForeignKey("assemble_delivery_fees.id"))
    delivery_version = relationship("AssembleDeliveryFees", back_populates="rdc_items")
