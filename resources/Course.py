from flask import request
from flask_restful import Resource
from http import HTTPStatus
from main import app


class CourseController(Resource):

    def __init__(self, course):
        self.course = course
    
    def get(self, course_id):
        return self.course.get_course(course_id)
    
    @app.route('/sarasa', methods = ['POST'])
    def post(self):
        req = request.get_json()

        if len(req['course_name']) <= 3:
            return {'message': 'Name too short'}, HTTPStatus.BAD_REQUEST
        
        return self.course.add_course(req)
