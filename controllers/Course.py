from fastapi import status


class CourseController:

    def __init__(self, courseService):
        self.service = courseService

    def handleCreate(self, course_create_data):
        self.service.addCourse(course_create_data)
        return {"message": "Course created successfully", "status": status.HTTP_200_OK}

    def handleGet(self, course_id):
        course = self.service.getCourse(course_id)
        return {"info": course, "status": status.HTTP_200_OK}

    # ToDo: tenemos una lista de filtros y solo vamos a mostrar los cursos a los cuales se pueda suscribir el usuario
    # La otra lista de cursos que se podria llegar a obtener es la de los cursos que cree
    def handleGetCourses(self):
        courses = self.service.getCourses()
        return {"info": courses, "status": status.HTTP_200_OK}

    def handleDelete(self, courseId, userId):
        self.service.deleteCourse(courseId, userId)
        return {"message": "Course deleted correctly", "status": status.HTTP_200_OK}

    def handleEdit(self, courseId, courseNewInfo):
        self.service.editCourse(courseId, courseNewInfo)
        return {"message": "Course edited correctly", "status": status.HTTP_200_OK}

    def handleAddCollaborator(self, courseId, collaboratorId):
        self.service.addCollaborator(courseId, collaboratorId)
        return {"message": "Collaborator added correctly", "status": status.HTTP_200_OK}

    def handleRemoveCollaborator(self, courseId, collaboratorId):
        self.service.removeCollaborator(courseId, collaboratorId)
        return {"message": "Collaborator correctly removed", "status": status.HTTP_200_OK}