class CourseController:

    def __init__(self, courseService):
        self.service = courseService

    def handle_course_create_post(self, courseData):
        return self.service.add_course(courseData)

    def handle_get_course(self, course_id):
        return self.service.get_courses(course_id)

    def handle_get_courses(self):
        return self.service.get_courses()

    def handle_delete_course(self, course_id):
        return self.service.delete_course(course_id)
