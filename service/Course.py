from http import HTTPStatus


class CourseService:
    def __init__(self, database):
        self.db = database

    def addCourse(self, courseInfo):
        return self.db.addCourse(courseInfo)

    def getCourse(self, courseId):
        return self.db.getCourse(courseId)

    def getCourses(self):
        return self.db.getCourses()

    def deleteCourse(self, courseId, userId):
        self.db.deleteCourse(courseId, userId)

    def editCourseInfo(self, courseId, newCourseInfo):
        self.db.editCourse(newCourseInfo, courseId)


# ErrorHandler ver que onda
