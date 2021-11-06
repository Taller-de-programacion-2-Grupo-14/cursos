from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from persistence.local import DB
from service.Course import CourseService
from controllers.Course import CourseController
from schemas.Schemas import *
from exceptions.CourseException import CourseException

app = FastAPI()
courseService = CourseService(DB())
courseController = CourseController(courseService)


@app.post('/courses/create')
def createCourse(createCourseData: CreateCourseSchema):
    return courseController.handleCreate(createCourseData.dict())


@app.get('/courses/{course_id}')
def getCourse(course_id: int):
    return courseController.handleGet(course_id)


@app.get('/courses')
def getCourses():
    return courseController.handleGetCourses()


@app.patch('/courses/{course_id}')
def editCourse(course_id: int, courseNewInfo: EditCourseInfoSchema):
    return courseController.handleEdit(course_id, courseNewInfo.dict())


@app.delete('/courses/{course_id}')
def deleteCourse(course_id: int, deleteCourseData: DeleteCourseSchema):
    return courseController.handleDelete(course_id, deleteCourseData.dict()['user_id'])


@app.post('courses/collaborators/{course_id}')
def addCollaborator(course_id: int, collaborator: CollaboratorSchema):
    courseController.handleAddCollaborator(course_id, collaborator.dict())


@app.delete('courses/collaborators/{course_id}')
def removeCollaborator(course_id: int, collaborator: CollaboratorSchema):
    courseController.handleRemoveCollaborator(course_id, collaborator.dict())


@app.exception_handler(RequestValidationError)
def validationExceptionHandler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors(),
                                  "body": exc.body,
                                  "your_additional_errors": {"Will be": "Inside", "This": " Error message"}})
    )


@app.exception_handler(CourseException)
def handle_course_exception(request: Request, exc: CourseException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"message": exc.message, "status": exc.status_code})
    )


@app.exception_handler(Exception)
def handleUnknownException(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=jsonable_encoder(
            {"message": 'Neither God knows what happened... just kidding, the error was:' + type(exc).__name__,
             "status": status.HTTP_503_SERVICE_UNAVAILABLE
             })
    )