from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from models.database import Base


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
