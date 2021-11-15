from fastapi import status


class CourseController:
    def __init__(self, courseService):
        self.service = courseService

    def handleCreate(self, course_create_data):
        self.service.addCourse(course_create_data)
        return {"message": "Course created successfully", "status": status.HTTP_200_OK}

    def handleGet(self, course_id):
        course = self.service.getCourse(course_id)
        return {"message": course, "status": status.HTTP_200_OK}

    def handleGetCourses(self, courseFilters):
        print(courseFilters) # ToDo: Delete me
        # ToDo: si queremos los cursos creados por deberiamos tener el id
        # que le corresponde a esa persona
        courses = self.service.getCourses(courseFilters)
        return {"message": courses, "status": self._getCorrectStatus(courses)}

    def handleDelete(self, deleteCourse):
        self.service.deleteCourse(deleteCourse)
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
        # Fixme: dudo que ande esto
        myCourses = self.service.getCourses({'creator_id': userId})
        return {"message": myCourses, "status": self._getCorrectStatus(myCourses)}

    def handleGetMySubscriptions(self, userId):
        mySubscriptions = self.service.getMySubscriptions(userId)
        return {"message": mySubscriptions, "status": self._getCorrectStatus(mySubscriptions)}

    def _getCorrectStatus(self, array):
        return status.HTTP_200_OK if len(array) else status.HTTP_204_NO_CONTENT
