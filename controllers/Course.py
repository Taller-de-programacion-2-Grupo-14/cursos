from fastapi import status
from service.Course import CourseService


class CourseController:
    def __init__(self, courseService: CourseService):
        self.service = courseService

    def handleCreate(self, course_create_data):
        self.service.addCourse(course_create_data)
        return {"message": "Course created successfully", "status": status.HTTP_200_OK}

    def handleGetCourse(self, courseId, userId):
        course = self.service.getCourse(courseId, userId)
        return {"message": course, "status": status.HTTP_200_OK}

    def handleGetCourses(self, userId, courseFilters):
        return self._getListCoursesResponse(
            self.service.getCourses(userId, courseFilters)
        )

    def handleCancel(self, courseId, userId):
        self.service.cancelCourse(courseId, userId)
        return {"message": "Course deleted correctly", "status": status.HTTP_200_OK}

    def handleEdit(self, courseNewInfo):
        self.service.editCourse(courseNewInfo)
        return {"message": "Course edited correctly", "status": status.HTTP_200_OK}

    def handleAddCollaborator(self, collaborator):
        self.service.addCollaborator(collaborator)
        return {"message": "Collaborator added correctly", "status": status.HTTP_200_OK}

    def handleRemoveCollaborator(self, removeCollaborator):
        self.service.removeCollaborator(removeCollaborator)
        return {
            "message": "Collaborator correctly removed",
            "status": status.HTTP_200_OK,
        }

    def handleSendCollaborationRequest(self, collaborationRequest):
        response = self.service.sendCollaborationRequest(collaborationRequest)
        return {
            "message": f"message {response} sent correctly",
            "status": status.HTTP_200_OK,
        }

    def handleAddSubscriber(self, courseId, subscriberId):
        self.service.addSubscriber(courseId, subscriberId)
        return {"message": "Successful subscription", "status": status.HTTP_200_OK}

    def handleRemoveSubscriber(self, courseId, subscriberId):
        self.service.removeSubscriber(courseId, subscriberId)
        return {"message": "Successful unsubscription", "status": status.HTTP_200_OK}

    def handleGetMyCourses(self, userId):
        return self._getListCoursesResponse(self.service.getMyCourses(userId))

    def handleGetMyCollaborations(self, userId, courseFilters):
        return self._getListCoursesResponse(
            self.service.getMyCollaborations(userId, courseFilters)
        )

    def handleGetMySubscriptions(self, userId):
        return self._getListCoursesResponse(self.service.getMySubscriptions(userId))

    def handleGetCourseUsers(self, courseId, userId, usersFilters):
        return self._getListCoursesResponse(
            self.service.getUsers(courseId, userId, usersFilters)
        )

    def handleBlockCourse(self, courseId, userId):
        self.service.blockCourse(courseId, userId)
        return {"message": "Course blocked correctly", "status": status.HTTP_200_OK}

    def handleUnblockCourse(self, courseId, userId):
        self.service.unblockCourse(courseId, userId)
        return {"message": "Course unblocked correctly", "status": status.HTTP_200_OK}

    def handleAddFavoriteCourse(self, favCourse):
        self.service.addFavoriteCourse(favCourse)
        return {
            "message": "Course added correctly to your Favorites",
            "status": status.HTTP_200_OK,
        }

    def handleGetFavoriteCourses(self, userId, courseFilters):
        return self._getListCoursesResponse(
            self.service.getFavoriteCourses(userId, courseFilters)
        )

    def handleRemoveFavoriteCourse(self, removeFavCourse):
        self.service.removeFavoriteCourse(removeFavCourse)
        return {
            "message": "Course removed correctly from your Favorites",
            "status": status.HTTP_200_OK,
        }

    def handleGetHistorical(self, userId, historicalFilters):
        return self._getListCoursesResponse(
            self.service.getHistorical(userId, historicalFilters)
        )

    def handleUpdateSubscriberStatus(self, subscriberGrades):
        self.service.updateSubscriberStatus(subscriberGrades)

    def handleSendNotification(self, notification):
        response = self.service.sendNotification(notification)
        return {
            "message": f"message {response} sent correctly",
            "status": status.HTTP_200_OK,
        }

    def _getListCoursesResponse(self, coursesList):
        return {"message": coursesList, "status": self._getCorrectStatus(coursesList)}

    def _getCorrectStatus(self, array):
        return status.HTTP_200_OK if len(array) else status.HTTP_204_NO_CONTENT
