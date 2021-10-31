from fastapi import FastAPI
from persistence.local import DB
from service.Course import CourseService
from controllers.Course import CourseController
from schemas.CreateCourseSchema import CreateCourseSchema
from http import HTTPStatus

app = FastAPI()
courseService = CourseService(DB())
courseController = CourseController(courseService)


@app.post('/course/create')
def create_course(createCourseData: CreateCourseSchema):
    courseController.handleCoursePost(createCourseData.dict())
    return {'message': 'Course created Correctly', 'status': HTTPStatus.OK}


@app.get('/course/{course_id}')
def get_course(course_id: int):
    return courseController.handleGetCourse(course_id)


@app.get('/courses')
def get_courses():
    return courseController.handleGetCourses()


@app.delete('/course/{course_id}')
def delete_course(course_id: int):
    return courseController.handleDeleteCourse(course_id)
