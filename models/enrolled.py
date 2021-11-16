# from sqlalchemy import CheckConstraint
from sqlalchemy import Integer, String, Column, ForeignKey, PrimaryKeyConstraint
from models.database import Base


class Enrolled(Base):
    __tablename__ = "enrolled"
    id_course = Column(Integer, ForeignKey("courses.id", on_delete="CASCADE"))
    id_student = Column(Integer)
    status = Column(String)
    __table_args__ = (PrimaryKeyConstraint("id_student", "id_course", name="id"), )
