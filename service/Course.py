from requests import HTTPError
from exceptions.CourseException import *

DEFAULT_OFFSET = 0
DEFAULT_LIMIT = 10


class CourseService:
    def __init__(self, database, usersClient):
        self.db = database
        self.userClient = usersClient

    def addCourse(self, courseInfo):
        courseNames = self._getCourseNames(
            self.db.getCourses(
                self._createDefaultFilter({"creator_id": courseInfo["user_id"]})
            )
        )
        if courseInfo["name"] in courseNames:
            raise CourseAlreadyExists(courseInfo["name"])
        self.db.addCourse(courseInfo)

    def getCourse(self, courseId, userId):
        self._raiseExceptionIfCourseDoesNotExists(courseId)
        course = self.db.getCourse(courseId)
        if course["cancelled"] and course["creator_id"] != userId:
            return []
        course["creator_name"] = self.mapIdsToNames([course["creator_id"]])[0]
        del course["creator_id"]
        return course

    def getCourses(self, courseFilters):
        courses = self.db.getCourses(courseFilters)
        result = []
        for course in courses:
            course["creator_name"] = self.mapIdsToNames([course["creator_id"]])[0]
            del course["creator_id"]
            result.append(course)
        return result

    def deleteCourse(self, deleteCourse):
        self._raiseExceptionIfCourseDoesNotExists(deleteCourse["id"])
        self._raiseExceptionIfIsNotTheCourseCreator(deleteCourse)
        self.db.deleteCourse(deleteCourse)

    def editCourse(self, courseNewInfo):
        self._raiseExceptionIfCourseDoesNotExists(courseNewInfo["id"])
        self._raiseExceptionIfIsNotTheCourseCreator(courseNewInfo)
        self.db.editCourse(courseNewInfo)

    def addCollaborator(self, collaborator):
        self._raiseExceptionIfCourseDoesNotExists(collaborator["id"])
        if collaborator["user_id"] in self.db.getCourseCollaborators(
            collaborator["id"]
        ):
            raise IsAlreadyACollaborator(self._getCourseName(collaborator["id"]))
        self.db.addCollaborator(collaborator)

    def removeCollaborator(self, removeCollaborator):
        self._raiseExceptionIfCourseDoesNotExists(removeCollaborator["id"])
        if removeCollaborator["user_to_remove"] not in self.db.getCourseCollaborators(
            removeCollaborator["id"]
        ):
            raise IsNotACollaborator(self._getCourseName(removeCollaborator["id"]))
        if removeCollaborator["user_id"] == removeCollaborator[
            "user_to_remove"
        ] or self._isTheCourseCreator(removeCollaborator):
            self.db.removeCollaborator(removeCollaborator)
        else:
            raise InvalidUserAction

    def addSubscriber(self, courseId, subscriberId):
        self._raiseExceptionIfCourseDoesNotExists(courseId)
        # if subscriberId in self.db.getSubscribers(courseId):
        #     raise IsAlreadySubscribed
        self.db.addSubscriber(courseId, subscriberId)

    def removeSubscriber(self, courseId, subscriberId):
        self._raiseExceptionIfCourseDoesNotExists(courseId)
        # if subscriberId not in self.db.getSubscribers(courseId):
        #     raise IsNotSubscribed
        self.db.removeSubscriber(courseId, subscriberId)

    def getMySubscriptions(self, userId):
        mySubscriptions = self.db.getMySubscriptions(userId)
        result = []
        for course in mySubscriptions:
            course["creator_name"] = self.mapIdsToNames([course["creator_id"]])[0]
            del course["creator_id"]
            result.append(course)
        return result

    def getUsers(self, courseId, userId, usersFilters):
        self._raiseExceptionIfCourseDoesNotExists(courseId)
        self._raiseExceptionIfIsNotTheCourseCreator({"id": courseId, "user_id": userId})
        userIds = self._parseResult(self.db.getUsers(courseId, usersFilters))
        return self.mapIdsToNames(userIds)

    def getMyCourses(self, userId):
        return self.db.getMyCourses(userId)

    # Auxiliar Functions
    def _getCourseNames(self, courses):
        names = set()
        for course in courses:
            names.add(course["name"])
        return names

    def _raiseExceptionIfCourseDoesNotExists(self, courseId):
        if self.db.getCourse(courseId) is None:
            raise CourseDoesNotExist

    def _raiseExceptionIfIsNotTheCourseCreator(self, courseData):
        if courseData["user_id"] != self.db.getCourse(courseData["id"])["creator_id"]:
            raise InvalidUserAction

    def _isTheCourseCreator(self, courseData):
        return (
            courseData["user_id"] == self.db.getCourse(courseData["id"])["creator_id"]
        )

    def _createDefaultFilter(self, filters):
        filter = {}
        for filterName, value in filters.items():
            filter[filterName] = value
        return {"filters": filter, "offset": DEFAULT_OFFSET, "limit": DEFAULT_LIMIT}

    def _getCourseName(self, courseId):
        return self.db.getCourse(courseId)["name"]

    def mapIdsToNames(self, userIds):
        info = self.getBatchUsers(userIds)
        users = []
        for user in info:
            users.append(user.get("first_name", ""))
        return users

    def getUser(self, userId):
        try:
            return self.userClient.getUser(userId)
        except HTTPError as e:
            print(f"exception while getting user f{e}")
            raise UserNotFound()

    def _parseResult(self, users):
        result = []
        for user in users:
            if "id_student" in user:
                result.append(user["id_student"])
            else:
                result.append(user["id_colaborator"])
        return result

    def getBatchUsers(self, ids: list):
        return self.userClient.getBatchUsers(ids).get("users", [])
