from sqlalchemy import Column, String, Float, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
from datetime import datetime

# 使用新的 DeclarativeBase


class Base(DeclarativeBase):
    pass


class DAS(Base):
    __tablename__ = "das"


class Oversize(Base):
    __tablename__ = "oversize"


class AHS(Base):
    __tablename__ = "ahs"


class GD(Base):
    __tablename__ = "GD"


class ResiC(Base):
    __tablename__ = "ResiC"
