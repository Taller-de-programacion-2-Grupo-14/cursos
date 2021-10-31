from flask import request
from flask_restful import Resource
from http import HTTPStatus

class CourseController(Resource):
    def __init__(self, service):
        self.service = service
        
    def post(self):
        data = request.get_json()
        data = {
            'courseName': data['course_name'],
            'courseDescription': data['course_description']}
        #     'hashtags': data['hashtags'],
        #     'courseType': data['course_type'],
        #     'amountExams': data['amount_exams'],
        #     'subscription': data['subscription'],
        #     'location': data['location']
        # }
        if self._checkData(data):
            print(self.service)
            # self.service.create_course(data)

        else:
            return {'msg': 'todo bad', 'status': 400}

        return {'msg': 'todo ok', 'status': 200}

    def _checkData(self, data):
        for key, value in data.items():
            if len(value) < 3:
                return False
        return True
