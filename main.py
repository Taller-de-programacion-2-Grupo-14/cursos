import os
from fastapi import FastAPI, Request, status, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from external.exams import Exams
from external.users import Users
from persistence.postgre import DB
from service.Course import CourseService
from controllers.Course import CourseController
from schemas.Schemas import *
from exceptions.CourseException import CourseException
from queryParams.QueryParams import *
from sqlalchemy import create_engine
import yaml
from notifications.NotificationManager import NotificationManager

dbUrl = os.environ.get("DATABASE_URL")
if not dbUrl.startswith("postgresql"):
    dbUrl = dbUrl.replace("postgres", "postgresql", 1)
print(f"url to connect is: {dbUrl}")
engine = create_engine(dbUrl, echo=True, future=True)
app = FastAPI()
userSearcher = Users()
examsClient = Exams()
notificationManager = NotificationManager()
courseService = CourseService(DB(engine), userSearcher, examsClient, notificationManager)
courseController = CourseController(courseService)


@app.post("/courses/create")
def createCourse(createCourseData: CreateCourseSchema):
    return courseController.handleCreate(createCourseData.dict())


@app.get("/courses/{courseId}/view")
def getCourse(courseId: int, user: UserSchema):
    return courseController.handleGetCourse(courseId, user.user_id)


@app.get("/courses")
def getCourses(
    user: UserSchema, courseFilters: CourseQueryParams = Depends(CourseQueryParams)
):
    return courseController.handleGetCourses(user.user_id, courseFilters.getFilters())


@app.patch("/courses/{courseId}")
def editCourse(courseId: int, courseNewInfo: EditCourseInfoSchema):
    courseNewInfo = courseNewInfo.dict()
    courseNewInfo["id"] = courseId
    return courseController.handleEdit(courseNewInfo)


@app.delete("/courses/{courseId}")
def cancelCourse(courseId: int, user: UserSchema):
    return courseController.handleCancel(courseId, user.user_id)


@app.post("/courses/collaborators")
def addCollaborator(collaborator: CollaboratorSchema):
    return courseController.handleAddCollaborator(collaborator.dict())


@app.delete("/courses/collaborators/remove")
def removeCollaborator(collaborator: RemoveCollaboratorSchema):
    return courseController.handleRemoveCollaborator(collaborator.dict())


@app.post("/courses/collaborators/send_request")
def sendCollaborationRequest(collaborationRequest: CollaborationRequest):
    return courseController.handleSendCollaborationRequest(collaborationRequest.dict())


@app.post("/courses/subscription/{courseId}")
def addSubscriber(courseId: int, subscriber: UserSchema):
    return courseController.handleAddSubscriber(courseId, subscriber.user_id)


@app.delete("/courses/subscription/{courseId}")
def removeSubscriber(courseId: int, subscriber: UserSchema):
    return courseController.handleRemoveSubscriber(courseId, subscriber.user_id)


@app.get("/courses/my_courses")
def getMyCourses(user: UserSchema):
    return courseController.handleGetMyCourses(user.user_id)


@app.get("/courses/my_subscriptions")
def getMySubscriptions(user: UserSchema):
    return courseController.handleGetMySubscriptions(user.user_id)


@app.get("/courses/my_collaborations")
def getMyCollaborations(
    user: UserSchema, courseFilters: CourseQueryParams = Depends(CourseQueryParams)
):
    return courseController.handleGetMyCollaborations(
        user.user_id, courseFilters.getFilters()
    )


@app.get("/courses/historical")
def getHistorical(
    user: UserSchema,
    historicalFilters: HistoricalQueryParams = Depends(HistoricalQueryParams),
):
    return courseController.handleGetHistorical(
        user.user_id, historicalFilters.getFilters()
    )


@app.get("/courses/users/{courseId}")
def getCourseUsers(
    courseId: int,
    user: UserSchema,
    usersFilters: UsersQueryParams = Depends(UsersQueryParams),
):
    return courseController.handleGetCourseUsers(
        courseId, user.user_id, usersFilters.getFilters()
    )


@app.delete("/courses/block/{courseId}")
def blockCourse(courseId: int, user: UserSchema):
    return courseController.handleBlockCourse(courseId, user.user_id)


@app.post("/courses/unblock/{courseId}")
def unblockCourse(courseId: int, user: UserSchema):
    return courseController.handleUnblockCourse(courseId, user.user_id)


@app.post("/courses/favorites")
def addFavoriteCourse(favCourse: FavCourseSchema):
    return courseController.handleAddFavoriteCourse(favCourse.dict())


@app.get("/courses/favorites")
def getFavorites(
    user: UserSchema, courseFilters: CourseQueryParams = Depends(CourseQueryParams)
):
    return courseController.handleGetFavoriteCourses(
        user.user_id, courseFilters.getFilters()
    )


@app.delete("/courses/favorites/remove")
def removeFavorite(removeFavCourse: FavCourseSchema):
    return courseController.handleRemoveFavoriteCourse(removeFavCourse.dict())


@app.patch("courses/update_subscriber_status")
def updateSubscriberStatus(subscriberGrades: SubscriberGradesSchema):
    return courseController.handleUpdateSubscriberStatus(subscriberGrades.dict())


@app.post("/notification")
def sendNotification(notification: NotificationSchema):
    return courseController.handleSendNotification(notification.dict())


@app.get("courses/summary_information")
def getSummaryInformation(summary: SummarySchema):
    return courseController.handleGetSummaryInformation(summary.dict())


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
