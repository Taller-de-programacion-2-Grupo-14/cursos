from sqlalchemy import Integer, Column, ForeignKey, PrimaryKeyConstraint
from models.database import Base


class FavoriteCourses(Base):
    __tablename__ = "favoritecourses"
    course_id = Column(Integer, ForeignKey("courses.id", on_delete="CASCADE"))
    user_id = Column(Integer)
    __table_args__ = (PrimaryKeyConstraint("course_id", "user_id", name="id"),)
