from requests import HTTPError
from typing import List
from exceptions.CourseException import *
from external.users import Users
from persistence.postgre import DB
from validator.CourseValidator import CourseValidator


class CourseService:
    def __init__(self, database: DB, usersClient: Users):
        self.db = database
        self.userClient = usersClient
        self.courseValidator = CourseValidator(database)

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
        if not self.courseValidator.canViewCourse(course, userId):
            raise CourseDoesNotExist
        creatorData = self.getUserData(course["creator_id"])
        self._addExtraData(course, creatorData, userId)
        return course

    def getCourses(self, userId, courseFilters):
        courses = self.db.getCourses(courseFilters)
        result = []
        creatorsData = self._getCreatorsData(courses)
        for course in courses:
            # ToDo: mostramos los cancelados por mas que seas el creador aca o no?
            if not self.courseValidator.canViewCourse(course, userId):
                continue
            creatorData = creatorsData[course["creator_id"]]
            if self._filterUserByName(courseFilters, creatorData, prefix="creator_"):
                continue
            self._addExtraData(course, creatorData, userId)
            result.append(course)
        return result

    def deleteCourse(self, courseId, userId):
        self.courseValidator.raiseExceptionIfCourseDoesNotExists(courseId)
        self.courseValidator.raiseExceptionIfIsNotTheCourseCreator(courseId, userId)
        self.db.deleteCourse(courseId)

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
        result = []
        creatorsData = self._getCreatorsData(mySubscriptions)
        for course in mySubscriptions:
            creatorData = creatorsData[course["creator_id"]]
            self._addExtraData(course, creatorData, userId)
            result.append(course)
        return result

    def getUsers(self, courseId, userId, usersFilters):
        self.courseValidator.raiseExceptionIfCourseDoesNotExists(courseId)
        self.courseValidator.raiseExceptionIfIsNotTheCourseCreator(courseId, userId)
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

    def getFavoriteCourses(self, userId):
        favCourses = self.db.getFavoriteCourses(userId)
        result = []
        creatorsData = self._getCreatorsData(favCourses)
        for course in favCourses:
            creatorData = creatorsData[course["creator_id"]]
            self._addExtraData(course, creatorData, userId)
            result.append(course)
        return result

    def removeFavoriteCourse(self, removeFavCourse):
        courseId = removeFavCourse["id"]
        userId = removeFavCourse["user_id"]
        self.courseValidator.raiseExceptionIfCourseDoesNotExists(courseId)
        self.courseValidator.raiseExceptionIfCourseIsNotLiked(courseId, userId)
        self.db.removeFavoriteCourse(courseId, userId)

    # Auxiliary Functions
    def _addExtraData(self, courseData: dict, creatorData: dict, userId: int):
        if creatorData.get("user_id", 0) != userId:
            userData = self.getUserData(userId)
        else:
            userData = creatorData
        courseData["creator_first_name"] = creatorData["first_name"]
        courseData["creator_last_name"] = creatorData["last_name"]
        courseData["can_edit"] = userId == courseData["creator_id"]
        courseData["can_subscribe"] = (
            not self.courseValidator.isCancelled(courseData)
            and not courseData["can_edit"]
            and self.courseValidator.canSubscribe(courseData["id"], userData)
        )
        courseData["can_collaborate"] = not self.courseValidator.isCancelled(
            courseData
        ) and (
            not courseData["can_edit"]
            or self.courseValidator.canCollaborate(courseData["id"], userData)
        )

    def _getCreatorsData(self, courses):
        ids = set()
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

    def _filterUserByName(self, filters, user, prefix=""):
        if (
                filters.get(prefix + "first_name", "")
                and filters[prefix + "first_name"] != user["first_name"]
        ):
            return True
        if (
                filters.get(prefix + "last_name", "")
                and filters[prefix + "last_name"] != user["last_name"]
        ):
            return True
        return False
