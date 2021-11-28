from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import Integer
from models.database import Base


class Collaborators(Base):
    __tablename__ = "collaborators"
    id_collaborator = Column(Integer)
    id_course = Column(Integer, ForeignKey("courses.id", on_delete="CASCADE"))
    __table_args__ = (PrimaryKeyConstraint("id_collaborator", "id_course", name="id"),)
