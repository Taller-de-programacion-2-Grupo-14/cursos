from fastapi import status

DEFAULT_OFFSET = 0
DEFAULT_LIMIT = 10


class CourseController:
    def __init__(self, courseService):
        self.service = courseService

    def handleCreate(self, course_create_data):
        self.service.addCourse(course_create_data)
        return {"message": "Course created successfully", "status": status.HTTP_200_OK}

    def handleGet(self, courseId, userId):
        course = self.service.getCourse(courseId, userId)
        return {"message": course, "status": status.HTTP_200_OK}

    def handleGetCourses(self, courseFilters):
        courses = self.service.getCourses(courseFilters)
        return {"message": courses, "status": self._getCorrectStatus(courses)}

    def handleDelete(self, courseId, user):
        self.service.deleteCourse(courseId, user)
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

    def handleAddSubscriber(self, courseId, subscriberId):
        self.service.addSubscriber(courseId, subscriberId)
        return {"message": "Successful subscription", "status": status.HTTP_200_OK}

    def handleRemoveSubscriber(self, courseId, subscriberId):
        self.service.removeSubscriber(courseId, subscriberId)
        return {"message": "Successful unsubscription", "status": status.HTTP_200_OK}

    def handleGetMyCourses(self, userId):
        filter = {
            "filters": {"creator_id": userId},
            "offset": DEFAULT_OFFSET,
            "limit": DEFAULT_LIMIT,
        }
        myCourses = self.service.getCourses(filter)
        return {"message": myCourses, "status": self._getCorrectStatus(myCourses)}

    def handleGetMySubscriptions(self, userId):
        mySubscriptions = self.service.getMySubscriptions(userId)
        return {
            "message": mySubscriptions,
            "status": self._getCorrectStatus(mySubscriptions),
        }

    def handleGetCourseUsers(self, courseId, userId, usersFilters):
        users = self.service.getUsers(courseId, userId, usersFilters)
        return {"message": users, "status": self._getCorrectStatus(users)}

    def _getCorrectStatus(self, array):
        return status.HTTP_200_OK if len(array) else status.HTTP_204_NO_CONTENT
