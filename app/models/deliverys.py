from sqlalchemy import Column, String, Float, DateTime, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func


# 使用新的 DeclarativeBase
class Base(DeclarativeBase):
    pass


class AssembleDeliveryFees(Base):
    __tablename__ = "AssembleDeliveryFees"
    id = Column(Integer, primary_key=True, autoincrement=True)
    secoend_name = Column(String(50), nullable=False)
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    # 使用 relationship 定义与 Child 的关系
    base_rates = relationship("BaseRate", back_populates="assemble_delivery_fees")
    das_items = relationship("Das", back_populates="assemble_delivery_fees")
    oversize_items = relationship("Oversize", back_populates="assemble_delivery_fees")
    ahs_items = relationship("Ahs", back_populates="assemble_delivery_fees")


class BaseRate(Base):
    __tablename__ = "BaseRate"
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    rate_weight = Column(Integer, nullable=False)
    zone = Column(Integer, nullable=False)
    fees = Column(Float, nullable=False)
    delivery_version_id = Column(Integer, ForeignKey("AssembleDeliveryFees.id"))


class Das(Base):
    __tablename__ = "Das"
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    das_type = Column(String(50), nullable=False)
    gd_hd_type = Column(String(50), nullable=False)
    res_comm_type = Column(String(50), nullable=False)
    fees = Column(Float, nullable=False)
    delivery_version_id = Column(Integer, ForeignKey("AssembleDeliveryFees.id"))


class Oversize(Base):
    __tablename__ = "Oversize"
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    os_type = Column(String(50), nullable=False)
    gd_hd_type = Column(String(50), nullable=False)
    fees = Column(Float, nullable=False)
    delivery_version_id = Column(Integer, ForeignKey("AssembleDeliveryFees.id"))


class Ahs(Base):
    __tablename__ = "Ahs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    ahs_type = Column(String(50), nullable=False)
    gd_hd_type = Column(String(50), nullable=False)
    res_comm_type = Column(String(50), nullable=False)
    fees = Column(Float, nullable=False)
    delivery_version_id = Column(Integer, ForeignKey("AssembleDeliveryFees.id"))


# class GdAndHd(Base):
#     __tablename__ = "GdAndHd"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     create_time = Column(DateTime, nullable=False, server_default=func.now())


# class ResAndComm(Base):
#     __tablename__ = "ResAndComm"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     create_time = Column(DateTime, nullable=False, server_default=func.now())
