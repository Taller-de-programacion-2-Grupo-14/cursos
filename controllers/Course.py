class CourseController:

    def __init__(self, courseService):
        self.service = courseService

    def handleCoursePost(self, course_create_data):
        return self.service.addCourse(course_create_data)

    def handleGetCourse(self, course_id):
        return self.service.getCourse(course_id)

    def handleGetCourses(self):
        return self.service.getCourses()

    def handleDeleteCourse(self, courseId, userId):
        return self.service.deleteCourse(courseId, userId)

