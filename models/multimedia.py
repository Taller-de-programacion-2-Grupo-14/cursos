from sqlalchemy import Integer, String, DateTime, Column, ForeignKey, PrimaryKeyConstraint
from models.database import Base
from datetime import datetime


class Multimedia(Base):
    __tablename__ = "multimedia"
    course_id = Column(Integer, ForeignKey("courses.id", on_delete="CASCADE"))
    title = Column(String(255))
    tag = Column(String(255))
    url = Column(String(255))
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    __table_args__ = (PrimaryKeyConstraint("course_id", "url", name="id"),)
