import os
from fastapi import FastAPI, Request, status, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from external.users import Users
from persistence.postgre import DB
from service.Course import CourseService
from controllers.Course import CourseController
from schemas.Schemas import *
from exceptions.CourseException import CourseException
from queryParams.QueryParams import *
from sqlalchemy import create_engine
import yaml


# engine = create_engine(
#     "postgresql://postgres:postgres@localhost:5432/test_db", echo=True, future=True
# )
engine = create_engine(os.environ.get("DATABASE_URL"), echo=True, future=True)
app = FastAPI()
userSearcher = Users()
courseService = CourseService(DB(engine), userSearcher)
courseController = CourseController(courseService)


@app.post("/courses/create")
def createCourse(createCourseData: CreateCourseSchema):
    return courseController.handleCreate(createCourseData.dict())


@app.get("/courses/{courseId}")
def getCourse(courseId: int, user: UserSchema):
    return courseController.handleGet(courseId, user.user_id)


@app.get("/courses")
def getCourses(courseFilters: CourseQueryParams = Depends(CourseQueryParams)):
    return courseController.handleGetCourses(courseFilters.getFilters())


@app.patch("/courses")
def editCourse(courseNewInfo: EditCourseInfoSchema):
    return courseController.handleEdit(courseNewInfo.dict())


@app.delete("/courses")
def deleteCourse(deleteCourseData: DeleteCourseSchema):
    return courseController.handleDelete(deleteCourseData.dict())


@app.post("/courses/collaborators")
def addCollaborator(collaborator: CollaboratorSchema):
    return courseController.handleAddCollaborator(collaborator.dict())


@app.delete("/courses/collaborators")
def removeCollaborator(collaborator: RemoveCollaboratorSchema):
    return courseController.handleRemoveCollaborator(collaborator.dict())


@app.post("courses/subscription/{courseId}")
def addSubscriber(courseId: int, subscriber: UserSchema):
    return courseController.handleAddSubscriber(courseId, subscriber.user_id)


@app.delete("courses/subscription/{courseId}")
def removeSubscriber(courseId: int, subscriber: UserSchema):
    return courseController.handleRemoveSubscriber(courseId, subscriber.user_id)


@app.get("courses/my_courses")
def getMyCourses(user: UserSchema):
    return courseController.handleGetMyCourses(user.user_id)


@app.get("courses/my_subscriptions")
def getMySubscriptions(user: UserSchema):
    return courseController.handleGetMySubscriptions(user.user_id)


@app.get("courses/users/{courseId}")
def getCourseUsers(courseId: int, user: UserSchema, usersFilters: UsersQueryParams):
    return courseController.handleGetCourseUsers(courseId, user.user_id, usersFilters)


@app.get("/doc-yml")
def getSwagger():
    with open("docs/swagger.yaml") as f:
        swagger = yaml.safe_load(f)
        return swagger


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    return response


@app.exception_handler(RequestValidationError)
def validationExceptionHandler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    fields = []
    for err in errors:
        value = {
            "field": err.get("loc", ["invalid field"])[-1],
            "message": err.get("msg", ""),
        }
        fields.append(value)
    finalStatus = status.HTTP_400_BAD_REQUEST
    return JSONResponse(
        status_code=finalStatus,
        content=jsonable_encoder({"errors": fields, "status": finalStatus}),
    )


@app.exception_handler(CourseException)
def handle_course_exception(request: Request, exc: CourseException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"message": exc.message, "status": exc.status_code}),
    )


@app.exception_handler(Exception)
def handleUnknownException(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=jsonable_encoder(
            {
                "message": f"Unknown error: {type(exc).__name__} with message: {exc.args[0]}",
                "status": status.HTTP_503_SERVICE_UNAVAILABLE,
            }
        ),
    )
