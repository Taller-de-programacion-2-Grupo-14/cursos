class DB:
    def __init__(self):
        self.db = {}
        self.id = 1

    def addCourse(self, courseData):
        if courseData['course_name'] in self._getCourseNames():
            raise ZeroDivisionError  # solo para probar algo
        self.db[self.id] = courseData
        self.id += 1

    def getCourse(self, courseId):
        if not self._courseExists(courseId):
            raise Exception
        return self.db[courseId]

    def getCourses(self):
        return self.db.values()

    def deleteCourse(self, courseId, userId):
        if not self._courseExists(courseId):
            raise Exception

        if not self._isTheCourseCreator(courseId, userId):
            raise Exception

        del self.db[courseId]

    def editCourse(self, newCourseInfo, courseId):
        if not self._courseExists(courseId):
            raise Exception
        self.db[courseId] = newCourseInfo  # No es tan asi, solo cierta info podemos modificar

    def _getCourseNames(self):
        names = []
        for courseInfo in self.db.values():
            names.append(courseInfo['course_name'])

        return names

    def _courseExists(self, courseId):
        return courseId in self.db

    def _isTheCourseCreator(self, userId, courseId):
        return self.db[courseId]['user_id'] == userId
