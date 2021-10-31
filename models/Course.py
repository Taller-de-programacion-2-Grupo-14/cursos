from http import HTTPStatus


class Course:
    def __init__(self, database):
        self.id = 0
        self.db = database
   
    def add_course(self, course_info):
        if course_info['course_name'] in self.db.values():
            return {'message': 'El curso ya existe'}, HTTPStatus.BAD_REQUEST
        self.db[self.id] = course_info['course_name']
        self.id += 1
        return {'message': 'Course created correctly'}, HTTPStatus.OK
    
    def get_course(self, course_id):
        course = self.db.get(course_id, None)
        if course is None:
            return {'message': 'Course not found'}, HTTPStatus.NOT_FOUND
        return self.db[course_id], HTTPStatus.OK
    
    def modify_course_info(self, course_id, new_course_info):
        course = self.db.get([course_id], None)

        if course is None:
            return {'message': 'Course not found'}, HTTPStatus.NOT_FOUND
        
        self.db[course_id] = new_course_info['course_name']
        
