from persistence.postgre import DB
from exceptions.CourseException import *

COURSE_SUBSC = {"basico": 1, "estandar": 2, "premium": 3}
USER_SUBS = {"free": 1, "platinum": 2, "black": 3}


class CourseValidator:
    def __init__(self, database: DB):
        self.db = database

    def hasACourseWithTheSameName(self, courseName, creatorId):
        filter = {"filters": {"creator_id": creatorId}}
        for course in self.db.getCourses(filter):
            if course.get("name", "") == courseName:
                return True
        return False

    def courseExists(self, courseId: int):
        return self.db.getCourse(courseId) is not None

    def isTheCourseCreator(self, courseData: dict):
        return (
            courseData["user_id"] == self.db.getCourse(courseData["id"])["creator_id"]
        )

    def isACollaborator(self, courseId: int, collaboratorId: int):
        filter = {"getSubscribers": False}
        return collaboratorId in self.db.getUsers(courseId, filter)

    def isSubscribed(self, courseId: int, subscriberId: int):
        filter = {"getSubscribers": True}
        return subscriberId in self.db.getUsers(courseId, filter)

    def canSubscribe(self, courseId: int, userInfo: dict):
        return self._canCollaborateOrSubscribe(courseId, userInfo)

    def canCollaborate(self, courseId: int, userInfo: dict):
        return self._canCollaborateOrSubscribe(courseId, userInfo, getSubscribers=False)

    def isCancelled(self, courseInfo: dict):
        return courseInfo.get("cancelled", 0)

    def raiseExceptionIfCourseDoesNotExists(self, courseId: int):
        if not self.courseExists(courseId):
            raise CourseDoesNotExist

    def raiseExceptionIfIsNotTheCourseCreator(self, courseData: dict):
        if not self.isTheCourseCreator(courseData):
            raise InvalidUserAction

    def _validateSubscription(self, userSubscription: str, courseSubscription: str):
        return (
            USER_SUBS[userSubscription.lower()]
            < COURSE_SUBSC[courseSubscription.lower()]
        )

    def canViewCourse(self, courseInfo, userId):
        return not(courseInfo["cancelled"] and courseInfo["creator_id"] != userId)

    def _canCollaborateOrSubscribe(self, courseId, userInfo: dict, getSubscribers=True):
        courseInfo = self.db.getCourse(courseId)
        if courseInfo is None:
            raise CourseDoesNotExist
        filter = {"subscribers": getSubscribers}
        return not(
            userInfo.get("blocked", True)
            or self._validateSubscription(
                userInfo.get("subscription"), courseInfo["subscription"]
            )
            or userInfo["id"] in self.db.getUsers(courseId, filter)
            or courseInfo["creator_id"] != userInfo["id"]
        )

