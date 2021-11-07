from exceptions.CourseException import *


class CourseService:
    def __init__(self, database):
        self.db = database

    def addCourse(self, courseInfo):
        if courseInfo['course_name'] in self.db.getCoursesCreatedBy(courseInfo['user_id']):
            raise CourseAlreadyExists(courseInfo['course_name'])
        return self.db.addCourse(courseInfo)

    def getCourse(self, courseId):
        course = self.db.getCourse(courseId)
        if course is None:
            raise CourseDoesNotExist
        return course

    def getCourses(self, courseFilters):
        return self.db.getCourses(courseFilters)

    def deleteCourse(self, deleteCourse):
        self._courseExists(deleteCourse)
        self._isTheCourseCreator(deleteCourse)
        self.db.deleteCourse(deleteCourse)

    def editCourseInfo(self, courseNewInfo):
        self._courseExists(courseNewInfo)
        self._isTheCourseCreator(courseNewInfo)
        self.db.editCourse(courseNewInfo)

    def addCollaborator(self, collaborator):
        self._courseExists(collaborator)
        if collaborator['user_id'] in self.db.getCourseCollaborators(collaborator['course_id']):
            raise IsAlreadyACollaborator(self.db.getCourseName(collaborator['course_id']))
        self.db.addCollaborator(collaborator)

    def removeCollaborator(self, removeCollaborator):
        self._courseExists(removeCollaborator)
        if removeCollaborator['user_to_remove'] not in \
                self.db.getCourseCollaborators(removeCollaborator['course_id']):
            raise IsNotACollaborator(self.db.getCourseName(removeCollaborator['course_id']))
        if removeCollaborator['user_id'] == removeCollaborator['user_to_remove'] \
                or self._isTheCourseCreator(removeCollaborator, raiseException=False):
            self.db.removeCollaborator(removeCollaborator)
        else:
            raise InvalidUserAction

    def _isTheCourseCreator(self, courseData, raiseException=True):
        if courseData['user_id'] == self.db.getCourseCreator(courseData['course_id']):
            return True

        if raiseException:
            raise InvalidUserAction
        return False

    def _courseExists(self, data):
        if self.db.getCourse(data['course_id']) is None:
            raise CourseDoesNotExist
