from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
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

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors(),
                                  "body": exc.body,
                                  "your_additional_errors": {"Will be": "Inside", "This": " Error message"}}),
    )

@app.exception_handler(ZeroDivisionError)
def validate_zero_handler(request: Request, exc: ZeroDivisionError):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({'detail': 'sarasa'})
    )
