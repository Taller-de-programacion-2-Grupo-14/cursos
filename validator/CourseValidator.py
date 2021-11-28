from persistence.postgre import DB
from exceptions.CourseException import *

COURSE_SUBSCRIPTION = {"basico": 1, "estandar": 2, "premium": 3}
USER_SUBSCRIPTION = {"free": 1, "platinum": 2, "black": 3}


class CourseValidator:
    def __init__(self, database: DB):
        self.db = database

    def hasACourseWithTheSameName(self, courseName, creatorId):
        for course in self.db.getCourses({"creator_id": creatorId}):
            if course.get("name", "") == courseName:
                return True
        return False

    def courseExists(self, courseId: int):
        return self.db.getCourse(courseId) is not None

    def isTheCourseCreator(self, courseId: int, userId: int):
        return userId == self.db.getCourse(courseId)["creator_id"]

    def isACollaborator(self, courseId: int, collaboratorId: int):
        filter = {"subscribers": False}
        return collaboratorId in self.db.getUsers(courseId, filter)

    def isSubscribed(self, courseId: int, subscriberId: int):
        filter = {"subscribers": True}
        return subscriberId in self.db.getUsers(courseId, filter)

    def canSubscribe(self, courseId: int, userData: dict):
        courseData = self.db.getCourse(courseId)
        if (
            userData["blocked"]
            or self.isSubscribed(courseId, userData["user_id"])
            or courseData["creator_id"] == userData["user_id"]
            or not self.hasCorrectSubscriptionType(
                courseData["subscription"], userData["subscription"]
            )
        ):
            return False
        return True

    def canCollaborate(self, courseId: int, userData: dict):
        if userData["blocked"] or self.isACollaborator(courseId, userData["user_id"]):
            return False
        return True

    def isCancelled(self, courseData: dict):
        return courseData.get("cancelled", 0)

    def isBlocked(self, courseId):
        course = self.db.getCourse(courseId)
        return course["blocked"]

    def hasCorrectSubscriptionType(
        self, courseSubscription: str, userSubscription: str
    ):
        return USER_SUBSCRIPTION.get(
            userSubscription.lower(), -1
        ) >= COURSE_SUBSCRIPTION.get(courseSubscription.lower(), -1)

    def canViewCourse(self, courseData, userId):
        return not (courseData["cancelled"] and courseData["creator_id"] != userId)

    def raiseExceptionIfCourseDoesNotExists(self, courseId: int):
        if not self.courseExists(courseId):
            raise CourseDoesNotExist

    def raiseExceptionIfIsNotTheCourseCreator(self, courseId: int, userId: int):
        if not self.isTheCourseCreator(courseId, userId):
            raise InvalidUserAction

    def raiseExceptionIfCanNotSubscribe(self, courseId: int, userData: dict):
        courseData = self.db.getCourse(courseId)
        self.raiseExceptionIfUserIsBlocked(userData)
        if self.isSubscribed(courseId, userData["user_id"]):
            raise IsAlreadySubscribed
        if courseData["creator_id"] == userData["user_id"]:
            raise InvalidUserAction
        if not self.hasCorrectSubscriptionType(
            courseData["subscription"], userData["subscription"]
        ):
            raise SubscriptionInvalid
        return True

    def raiseExceptionIfCanNotCollaborate(self, courseId: int, userData: dict):
        self.raiseExceptionIfUserIsBlocked(userData)
        if self.isACollaborator(courseId, userData["user_id"]):
            raise IsAlreadyACollaborator
        return True

    def raiseExceptionIfUserIsBlocked(self, userData):
        if userData.get("blocked", False):
            raise UserBlocked

    # ToDo: completar metodos
    def raiseExceptionIfIsNotAdmin(self, userData):
        if not userData.get("is_admin", False):
            raise InvalidUserAction

    def raiseExceptionIfCourseIsAlreadyLiked(self, courseId, userId):
        if courseId in self.db.getCoursesLikedBy(userId):
            raise CourseIsAlreadyLiked

    def raiseExceptionIfCourseIsNotLiked(self, courseId, userId):
        if courseId not in self.db.getCoursesLikedBy(userId):
            raise CourseIsNotLiked
