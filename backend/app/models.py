from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from .database import Base
import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    total_area = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Territory(Base):
    __tablename__ = "territories"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    polygon = Column(Geometry("POLYGON", srid=4326))
    area = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)

    user = relationship("User")


class ActivityPoint(Base):
    __tablename__ = "activity_points"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"))
    lat = Column(Float)
    lon = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    activity = relationship("Activity")

