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
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    user_id = Column(String(36), ForeignKey(User.id))
    # 定义与 User 表的关系
    user = relationship("User", back_populates="assembleDeliveryFees")
    # 一对多表
    base_rates = relationship(
        "BaseRate", back_populates="delivery_version", cascade="all, delete-orphan"
    )
    das_items = relationship(
        "Das", back_populates="delivery_version", cascade="all, delete-orphan"
    )
    oversizes = relationship(
        "Oversize", back_populates="delivery_version", cascade="all, delete-orphan"
    )
    ahs_items = relationship(
        "Ahs", back_populates="delivery_version", cascade="all, delete-orphan"
    )
    rdc_items = relationship(
        "Rdc", back_populates="delivery_version", cascade="all, delete-orphan"
    )
    # 一对一表
    demand_charge = relationship(
        "DemandCharge",
        back_populates="delivery_version",
        uselist=False,
        cascade="all, delete-orphan",
    )


class BaseRate(Base):
    __tablename__ = "base_rate"
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime, server_default=func.now())
    rate_weight = Column(Integer, nullable=False)
    zone = Column(Integer, nullable=False)
    fees = Column(Float, nullable=False)
    delivery_version_id = Column(Integer, ForeignKey(AssembleDeliveryFees.id))
    delivery_version = relationship("AssembleDeliveryFees", back_populates="base_rates")


class Das(Base):
    __tablename__ = "das"
    id = Column(Integer, primary_key=True, autoincrement=True)
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
    create_time = Column(DateTime, server_default=func.now())
    gd_hd_type = Column(SqlEnum(GdAndHd), nullable=False)
    fees = Column(Float, nullable=False)

    delivery_version_id = Column(Integer, ForeignKey(AssembleDeliveryFees.id))
    delivery_version = relationship("AssembleDeliveryFees", back_populates="oversizes")


class Ahs(Base):
    __tablename__ = "ahs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime, server_default=func.now())
    ahs_type = Column(SqlEnum(AhsType), nullable=False)
    gd_hd_type = Column(SqlEnum(GdAndHd), nullable=False)
    res_comm_type = Column(SqlEnum(ResAndComm), nullable=False)
    fees = Column(Float, nullable=False)
    delivery_version_id = Column(Integer, ForeignKey(AssembleDeliveryFees.id))
    delivery_version = relationship("AssembleDeliveryFees", back_populates="ahs_items")


class Rdc(Base):
    __tablename__ = "rdc"
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime, server_default=func.now())
    gd_hd_type = Column(SqlEnum(GdAndHd), nullable=False)
    fees = Column(Float, nullable=False)
    delivery_version_id = Column(Integer, ForeignKey(AssembleDeliveryFees.id))
    delivery_version = relationship("AssembleDeliveryFees", back_populates="rdc_items")


class DemandCharge(Base):
    __tablename__ = "DemandCharge"
    id = Column(Integer, primary_key=True, autoincrement=True)
    DIM = Column(Integer, nullable=False, default=250)
    peak_os_charge = Column(Float, nullable=False, default=0)
    peak_rdc_charge = Column(Float, nullable=False, default=0)
    fuel_rate = Column(Float, nullable=False, default=0.15)
    create_time = Column(DateTime, server_default=func.now())
    delivery_version_id = Column(
        Integer, ForeignKey(AssembleDeliveryFees.id), unique=True
    )
    delivery_version = relationship(
        "AssembleDeliveryFees", back_populates="demand_charge"
    )
