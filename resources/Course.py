class CourseController:

    def __init__(self, courseService):
        self.service = courseService
    
    def handle_course_create_post(self, courseData):
        return self.service.add_course(courseData)
    
    def handle_get_course(self, course_id):
        return self.service.get_course(course_id)
