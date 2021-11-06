from fastapi import status


class CourseException(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


class CourseAlreadyExists(CourseException):
    def __init__(self, courseName):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = f"Course '{courseName}' already exists"


class CourseDoesNotExist(CourseException):
    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = "Course does not exist"


class InvalidUserAction(CourseException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = "Invalid user action"


class IsAlreadyACollaborator(CourseException):
    def __init__(self, courseName):
        self.status_code = status.HTTP_208_ALREADY_REPORTED
        self.message = f"The user is already a collaborator of the course '{courseName}'"


class IsNotACollaborator(CourseException):
    def __init__(self, courseName):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = f"The user is not a collaborator of the course '{courseName}'"
