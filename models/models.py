from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import Integer
from sqlalchemy import String
from .database import Base


class Courses(Base):
    __tablename__ = "courses"
    name = Column(String(255))
    id = Column(Integer, primary_key=True)
    exams = Column(Integer)
    creator_id = Column(Integer)
    category = Column(String(255))
    subscription = Column(String(255))
    description = Column(String(255))


class Colaborators(Base):
    __tablename__ = "colaborators"
    id_colaborator = Column(Integer)
    id_course = Column(Integer, ForeignKey("courses.id", on_delete="CASCADE"))
    __table_args__ = PrimaryKeyConstraint("id_colaborator", "id_course", name="id")


class Enrolled(Base):
    __tablename__ = "enrolled"
    id_course = Column(Integer, ForeignKey("courses.id", on_delete="CASCADE"))
    id_student = Column(Integer)
    status = Column(Integer)
    __table_args__ = PrimaryKeyConstraint("id_student", "id_course", name="id")
