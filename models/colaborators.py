from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import Integer
from models.database import Base


class Colaborators(Base):
    __tablename__ = "colaborators"
    id_colaborator = Column(Integer)
    id_course = Column(Integer, ForeignKey("courses.id", on_delete="CASCADE"))
    __table_args__ = (PrimaryKeyConstraint("id_colaborator", "id_course", name="id"),)
