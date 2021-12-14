from requests import HTTPError
from typing import List
from exceptions.CourseException import *
from external.users import Users
from notifications.NotificationManager import NotificationManager
from persistence.postgre import DB
from validator.CourseValidator import CourseValidator


class CourseService:
    def __init__(
        self, database: DB, usersClient: Users, notification: NotificationManager
    ):
        self.db = database
        self.userClient = usersClient
        self.courseValidator = CourseValidator(database)
        self.notification = notification

    def addCourse(self, courseInfo):
        if self.courseValidator.hasACourseWithTheSameName(
            courseInfo["name"], courseInfo["user_id"]
        ):
            raise CourseAlreadyExists(courseInfo["name"])
        self.db.addCourse(courseInfo)

    def getCourse(self, courseId, userId):
        course = self.db.getCourse(courseId)
        if course is None:
            raise CourseDoesNotExist
        usersData = self._getUsersData([course], userId)
        actualUserData = usersData[userId]
        if not self.courseValidator.canViewCourse(course, actualUserData):
            raise CourseDoesNotExist
        self._addExtraData(course, usersData[course["creator_id"]], actualUserData)
        return course

    def getCourses(self, userId, courseFilters):
        courses = self.db.getCourses(courseFilters)
        return self._filterCourses(courses, userId, courseFilters)

    def cancelCourse(self, courseId, userId):
        self.courseValidator.raiseExceptionIfCourseDoesNotExists(courseId)
        self.courseValidator.raiseExceptionIfIsNotTheCourseCreator(courseId, userId)
        # ToDo: send notificaction
        self.db.cancelCourse(courseId)

    def editCourse(self, courseNewInfo):
        self.courseValidator.raiseExceptionIfCourseDoesNotExists(courseNewInfo["id"])
        self.courseValidator.raiseExceptionIfIsNotTheCourseCreator(
            courseNewInfo["id"], courseNewInfo["user_id"]
        )
        actualCourseName = self._getCourseName(courseNewInfo["id"])
        if actualCourseName != courseNewInfo[
            "name"
        ] and self.courseValidator.hasACourseWithTheSameName(
            courseNewInfo["name"], courseNewInfo["user_id"]
        ):
            raise CourseAlreadyExists(courseNewInfo["name"])
        self.db.editCourse(courseNewInfo)

    def addCollaborator(self, collaborator):
        self.courseValidator.raiseExceptionIfCourseDoesNotExists(collaborator["id"])
        userData = self.getUserData(collaborator["user_id"])
        if self.courseValidator.raiseExceptionIfCanNotCollaborate(
            collaborator["id"], userData
        ):
            self.db.addCollaborator(collaborator)

    def removeCollaborator(self, removeCollaborator):
        self.courseValidator.raiseExceptionIfCourseDoesNotExists(
            removeCollaborator["id"]
        )
        userData = self.getUserData(removeCollaborator["user_id"])
        self.courseValidator.raiseExceptionIfUserIsBlocked(userData)
        if not self.courseValidator.isACollaborator(
            removeCollaborator["id"], removeCollaborator["user_to_remove"]
        ):
            raise IsNotACollaborator(self._getCourseName(removeCollaborator["id"]))
        if removeCollaborator["user_id"] == removeCollaborator[
            "user_to_remove"
        ] or self.courseValidator.isTheCourseCreator(
            removeCollaborator["id"], removeCollaborator["user_id"]
        ):
            self.db.removeCollaborator(removeCollaborator)
        else:
            raise InvalidUserAction

    def addSubscriber(self, courseId, subscriberId):
        self.courseValidator.raiseExceptionIfCourseDoesNotExists(courseId)
        subscriberData = self.getUserData(subscriberId)
        if self.courseValidator.raiseExceptionIfCanNotSubscribe(
            courseId, subscriberData
        ):
            self.db.addSubscriber(courseId, subscriberId)

    def removeSubscriber(self, courseId, subscriberId):
        self.courseValidator.raiseExceptionIfCourseDoesNotExists(courseId)
        subscriberData = self.getUserData(subscriberId)
        if self.courseValidator.raiseExceptionIfUserIsBlocked(subscriberData):
            raise UserBlocked
        if not self.courseValidator.isSubscribed(courseId, subscriberId):
            raise IsNotSubscribed
        self.db.removeSubscriber(courseId, subscriberId)

    def getMySubscriptions(self, userId):
        mySubscriptions = self.db.getMySubscriptions(userId)
        return self._filterCourses(mySubscriptions, userId)

    def getUsers(self, courseId, userId, usersFilters):
        self.courseValidator.raiseExceptionIfCourseDoesNotExists(courseId)
        userData = self.getUserData(userId)
        if not userData["is_admin"] and not self.courseValidator.isTheCourseCreator(
            courseId, userId
        ):
            raise InvalidUserAction
        userIds = self.db.getUsers(courseId, usersFilters)
        usersData = self.getUsersData(userIds)
        result = []
        for user in usersData:
            if self._filterUserByName(usersFilters, user):
                continue
            result.append(user)
        return result

    def getMyCourses(self, userId):
        return self.getCourses(userId, {"creator_id": userId})

    def blockCourse(self, courseId: int, userId: int):
        self.courseValidator.raiseExceptionIfCourseDoesNotExists(courseId)
        userData = self.userClient.getUser(userId)
        self.courseValidator.raiseExceptionIfIsNotAdmin(userData)
        if self.courseValidator.isBlocked(courseId):
            raise CourseIsAlreadyBlocked
        self.db.blockCourse(courseId)

    def unblockCourse(self, courseId: int, userId: int):
        self.courseValidator.raiseExceptionIfCourseDoesNotExists(courseId)
        userData = self.userClient.getUser(userId)
        self.courseValidator.raiseExceptionIfIsNotAdmin(userData)
        if not self.courseValidator.isBlocked(courseId):
            raise CourseIsNotBlocked
        self.db.unblockCourse(courseId)

    def addFavoriteCourse(self, favCourse):
        courseId = favCourse["id"]
        userId = favCourse["user_id"]
        self.courseValidator.raiseExceptionIfCourseDoesNotExists(courseId)
        self.courseValidator.raiseExceptionIfCourseIsAlreadyLiked(courseId, userId)
        self.db.addFavoriteCourse(courseId, userId)

    def getFavoriteCourses(self, userId, courseFilters):
        favCourses = self.db.getFavoriteCourses(userId, courseFilters)
        return self._filterCourses(favCourses, userId, courseFilters)

    def removeFavoriteCourse(self, removeFavCourse):
        courseId = removeFavCourse["id"]
        userId = removeFavCourse["user_id"]
        self.courseValidator.raiseExceptionIfCourseDoesNotExists(courseId)
        self.courseValidator.raiseExceptionIfCourseIsNotLiked(courseId, userId)
        self.db.removeFavoriteCourse(courseId, userId)

    def getMyCollaborations(self, userId, courseFilters):
        myCollaborations = self.db.getMyCollaborations(userId, courseFilters)
        return self._filterCourses(myCollaborations, userId, courseFilters)

    def getHistorical(self, userId, historicalFilters):
        courses = self.db.getHistorical(userId, historicalFilters)
        return self._filterCourses(courses, userId, historicalFilters)

    def sendCollaborationRequest(self, collaborationRequest):
        courseId = collaborationRequest["id"]
        self.courseValidator.raiseExceptionIfCourseDoesNotExists(courseId)
        self.courseValidator.raiseExceptionIfIsNotTheCourseCreator(
            courseId, collaborationRequest["user_id"]
        )
        userData = self.getUserData(collaborationRequest["email_collaborator"])
        # ToDo: chequear que no este mandando la solicitud a alguien que es colaborador o creador
        userToken = self.getUserToken(userData["user_id"])
        courseData = self.db.getCourse(courseId)
        # creatorName = (
        #     courseData["creator_last_name"] + ", " + courseData["creator_first_name"]
        # )
        creatorName = "Lichita"
        body = (
            f"Hola {userData['user_id']},"
            f"queres ser colaborador en el curso {courseData['name']} creado por {creatorName}?"
        )
        return self.notification.collaborationRequest(userToken, courseId, body)

    def sendNotification(self, notification):
        userToken = self.getUserToken(notification["user_id"])
        return self.notification.sendNotification(
            userToken, notification["title"], notification["body"]
        )

    def sendData(self, data):
        userId = data["user_id"]
        courseId = data["course_id"]
        return self.getCourse(courseId, userId)

    # Auxiliary Functions
    def _filterCourses(
        self, courses: List[dict], userId: int, courseFilters: dict = None
    ):
        result = []
        usersData = self._getUsersData(courses, userId)
        actualUserData = usersData[userId]
        for course in courses:
            if not self.courseValidator.canViewCourse(course, actualUserData):
                continue
            creatorData = usersData[course["creator_id"]]
            if self._filterUserByName(courseFilters, creatorData, prefix="creator_"):
                continue
            self._addExtraData(course, creatorData, actualUserData)
            result.append(course)
        return result

    def _addExtraData(self, courseData: dict, creatorData: dict, userData: dict):
        courseData["creator_first_name"] = creatorData["first_name"]
        courseData["creator_last_name"] = creatorData["last_name"]
        courseData["can_edit"] = userData["user_id"] == courseData["creator_id"]
        courseData["can_subscribe"] = self._canSubscribe(courseData, userData)
        courseData["can_collaborate"] = self._canCollaborate(courseData, userData)
        courseData["is_subscribed"] = self.courseValidator.isSubscribed(
            courseData["id"], userData["user_id"]
        )

    def _canEdit(self, courseData: dict, userData: dict):
        return (
            not userData["is_admin"]
            and not courseData["blocked"]
            and userData["user_id"] == courseData["creator_id"]
        )

    def _canSubscribe(self, courseData: dict, userData: dict):
        return (
            not userData["is_admin"]
            and self.courseValidator.isAvailable(courseData)
            and not courseData["can_edit"]
            and self.courseValidator.canSubscribe(courseData["id"], userData)
        )

    def _canCollaborate(self, courseData: dict, userData: dict):
        return (
            not userData["is_admin"]
            and self.courseValidator.isAvailable(courseData)
            and not courseData["can_edit"]
            and self.courseValidator.canCollaborate(courseData["id"], userData)
        )

    def _getUsersData(self, courses: List[dict], userId: int):
        # ToDo: rename this function
        ids = {userId}
        for course in courses:
            ids.add(course["creator_id"])
        result = self.getUsersData(list(ids))
        creatorsData = {}
        for creator in result:
            creatorsData[creator["user_id"]] = creator
        return creatorsData

    def _getCourseName(self, courseId):
        return self.db.getCourse(courseId)["name"]

    def getUserData(self, userId):
        try:
            return self.userClient.getUser(userId)
        except HTTPError as e:
            print(f"exception while getting user f{e}")
            raise UserNotFound()

    def getUsersData(self, userIds: List[int]):
        try:
            return self.userClient.getBatchUsers(userIds).get("users", [])
        except HTTPError as e:
            print(f"exception while getting user f{e}")
            raise UserNotFound()

    def getUserToken(self, userId: int):
        try:
            return self.userClient.getUserToken(userId).get("token", -1)
        except HTTPError as e:
            print(f"exception while getting user f{e}")
            raise UserNotFound()

    def _filterUserByName(self, filters, user, prefix=""):
        if filters is None:
            return False
        if (
            filters.get(prefix + "first_name", "")
            and filters[prefix + "first_name"].lower() != user["first_name"].lower()
        ):
            return True
        if (
            filters.get(prefix + "last_name", "")
            and filters[prefix + "last_name"].lower() != user["last_name"].lower()
        ):
            return True
        return False
