from sqlalchemy import Column, Integer, String, DateTime, Boolean
from models.database import Base
from datetime import datetime


class Courses(Base):
    __tablename__ = "courses"
    name = Column(String(255))
    id = Column(Integer, primary_key=True)
    exams = Column(Integer)
    creator_id = Column(Integer)
    type = Column(String(255))
    subscription = Column(String(255))
    description = Column(String(255))
    hashtags = Column(String(1000))
    location = Column(String(255))
    cancelled = Column(Integer)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    blocked = Column(Boolean(), default=False)
