from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import inspect
from sqlalchemy import Integer
from sqlalchemy import or_
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import with_polymorphic

Base = declarative_base()


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
    # __table_args__ = (PrimaryKeyConstraint('id_colaborator', 'id_course', name='id'))
    __table_args__ = (PrimaryKeyConstraint('id_colaborator', 'id_course', name='id'),)


class Enrolled(Base):
    __tablename__ = "enrolled"
    id_course = Column(Integer, ForeignKey("courses.id", on_delete="CASCADE"))
    id_student = Column(Integer)
    status = Column(Integer)
    __table_args__ = (PrimaryKeyConstraint('id_student', 'id_course', name='id'),)


engine = create_engine("postgresql://postgres:postgres@localhost:5432/test_db", echo=True)
# Base.metadata.create_all(engine)

session = Session(engine)
lucho_capo = session.query(Courses).get(1)
# c = Colaborators(id_colaborator=7, id_course=1)
# session.add(c)
# session.commit()
lucho_mas_capo = session.query(Colaborators).get((4, 1))
# course_a = Courses(name='luchooo', exams=5, creator_id=6, category='python8', subscription='free', description='lucho keeps surprising')
# session.add(course_a)
# session.commit()
lucho_el_mas_capo = session.query(Courses).get(2)
# lucho_f = session.delete(lucho_mas_capo)
session.commit()
# cuadno termine: poner session.commit
colabs_8 = session.query(Colaborators).filter(Colaborators.id_course == 8)
if not colabs_8.first():
    print("It worked!")
else:
    print("Bad news :(")
