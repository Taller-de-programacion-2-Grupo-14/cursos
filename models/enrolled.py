from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import Integer
from models.database import Base


class Enrolled(Base):
    __tablename__ = "enrolled"
    id_course = Column(Integer, ForeignKey("courses.id", on_delete="CASCADE"))
    id_student = Column(Integer)
    status = Column(Integer)
    __table_args__ = PrimaryKeyConstraint("id_student", "id_course", name="id")
