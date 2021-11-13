from exceptions.CourseException import *
from sqlalchemy.orm import Session
from ..models import Courses, Colaborators, Enrolled


class DB:
    def __init__(self, engine):
        self.session = Session(engine)

    def addCourse(self, courseInfo):
        name = courseInfo['name']
        exams = courseInfo['exams']
        creator_id = courseInfo['creator_id']
        category = courseInfo['category']
        subscription = courseInfo['subscription']
        description = courseInfo['description']
        c = Courses(name=name,
                    exams=exams,
                    creator_id=creator_id,
                    category=category,
                    subscription=subscription,
                    description=description)
        self.session.add(c)
        self.session.commit()

    def getCourse(self, courseId):
        course = self.session.query(Courses).get(courseId)
        if not course:
            return None
        dic_course = {'name': course.name,
                      'exams': course.exams,
                      'creator_id': course.creator_id,
                      'category': course.category,
                      'subscription': course.subscription,
                      'description': course.description}
        return dic_course

    def getCourses(self, courseFilters):
        return

    def deleteCourse(self, deleteCourse):
        course_id = deleteCourse["course_id"]
        course = self.session.query(Colaborators).get(course_id)
        if not course:
            return None
        self.session.delete(course)
        self.session.commit()

    def editCourse(self, courseNewInfo):
        return

    def addCollaborator(self, collaborator):
        # same remove
        return

    def removeCollaborator(self, collaborator):
        # if not _isTheCourseCreator(collaborator.id, course.id): el course_id
        #     raise InvalidUserAction
        return

    def _courseExists(self, courseId):
        course = self.session.query(Courses).get(courseId)
        return True if course else False

    def _isTheCourseCreator(self, userId, courseId):
        course = self.session.query(Colaborators).get((userId, courseId))
        return True if course else False

    def getCourseName(self, courseId):
        course = self.session.query(Courses).get(courseId)
        return course.name if course else None

    def getCourseCreator(self, courseId):
        course = self.session.query(Courses).get(courseId)
        return course.creator_id if course else None

    def getCoursesCreatedBy(self, user_id):
        courses_creator = self.session.query(Courses).filter(Courses.creator_id == user_id)
        if not courses_creator.first():
            return None
        courses = []
        for c in courses_creator:
            courses.append(c.name)
        return courses

    def getCourseCollaborators(self, courseId):
        colabs_course = self.session.query(Colaborators).filter(Colaborators.id_course == courseId)
        if not colabs_course.first():
            return None
        colaborators = []
        for c in colabs_course:
            colaborators.append(c.id_colaborator)
        return colaborators
