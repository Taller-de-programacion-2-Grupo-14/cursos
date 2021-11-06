from exceptions.CourseException import *


class DB:
    def __init__(self):
        self.db = {}
        self.collaboratorsDB = {}
        self.id = 1

    def addCourse(self, courseData):
        if courseData['course_name'] in self._getCourseNames():
            raise CourseAlreadyExists(courseData['course_name'])
        self.db[self.id] = courseData
        self.id += 1

    def getCourse(self, courseId):
        self._courseExists(courseId)
        return self.db[courseId]

    def getCourses(self):
        courses = []
        for course in self.db.values():
            courses.append(course)
        return courses

    def deleteCourse(self, courseId, userId):
        self._courseExists(courseId)
        if not self._isTheCourseCreator(courseId, userId):
            raise InvalidUserAction

        del self.db[courseId]

    def editCourse(self, courseId, courseNewInfo):
        self._courseExists(courseId)
        if not self._isTheCourseCreator(courseNewInfo['user_id'], courseId):
            raise InvalidUserAction

        self.db[courseId] = courseNewInfo  # No es tan asi, solo cierta info podemos modificar otra es fija

    def addCollaborator(self, courseId, collaboratorId):
        self._courseExists(courseId)
        if collaboratorId in self.collaboratorsDB[courseId]:
            raise IsAlreadyACollaborator(self._getCourseName(courseId))

        self.collaboratorsDB[courseId].append(collaboratorId)

    def removeCollaborator(self, courseId, collaboratorId):
        # ToDo: supongo que hay dos formas de dar de baja un colaborador.
        # 1) El creador lo saca 2) el colaborador se da de baja, verificar que se cumpla una de las dos
        self._courseExists(courseId)
        if collaboratorId not in self.collaboratorsDB[courseId]:
            raise IsNotACollaborator(self._getCourseName(courseId))

        self.collaboratorsDB[courseId].remove(collaboratorId)

    def _getCourseNames(self):
        names = []
        for courseInfo in self.db.values():
            names.append(courseInfo['course_name'])

        return names

    def _courseExists(self, courseId):
        if courseId not in self.db:
            raise CourseDoesNotExist

    def _isTheCourseCreator(self, userId, courseId):
        return self.db[courseId]['user_id'] == userId

    def _getCourseName(self, courseId):
        return self.db[courseId]['course_name']
