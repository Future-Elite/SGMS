import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class OperationTypeEnum(enum.Enum):
    click = "click"
    swipe = "swipe"
    zoom = "zoom"
    move = "move"


class DeviceTypeEnum(enum.Enum):
    light = "light"
    fan = "fan"
    tv = "tv"


class ResultEnum(enum.Enum):
    success = "success"
    fail = "fail"


class GestureMap(Base):
    __tablename__ = 'gesture_map'
    id = Column(Integer, primary_key=True, autoincrement=True)
    gesture_name = Column(String(50), unique=True, nullable=False)
    operation_type = Column(Enum(OperationTypeEnum), nullable=False)
    operation_param = Column(String(100), default='')
    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)


class DeviceState(Base):
    __tablename__ = 'device_state'
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_type = Column(Enum(DeviceTypeEnum), nullable=False)
    device_id = Column(String(100), nullable=False)
    current_state = Column(JSON, nullable=False)
    last_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class OperationLog(Base):
    __tablename__ = 'operation_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    gesture_id = Column(Integer, ForeignKey('gesture_map.id'))
    operation_type = Column(Enum(OperationTypeEnum), nullable=False)
    device_type = Column(Enum(DeviceTypeEnum), nullable=False)
    operation_time = Column(DateTime, default=datetime.now)
    result = Column(Enum(ResultEnum), nullable=False)
    detail = Column(String, default='')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    is_admin = Column(Boolean, default=False, nullable=False)
    password_salt = Column(String(32))
    password_hash = Column(String(64))
