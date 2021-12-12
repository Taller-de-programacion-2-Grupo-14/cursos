from fastapi import status


class CourseException(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


class CourseAlreadyExists(CourseException):
    def __init__(self, courseName):
        super().__init__(
            status.HTTP_400_BAD_REQUEST, f"Course '{courseName}' already exists"
        )


class CourseDoesNotExist(CourseException):
    def __init__(self):
        super().__init__(status.HTTP_404_NOT_FOUND, "Course does not exist")


class InvalidUserAction(CourseException):
    def __init__(self):
        super().__init__(status.HTTP_401_UNAUTHORIZED, "Invalid user action")


class IsAlreadyACollaborator(CourseException):
    def __init__(self):
        super().__init__(
            status.HTTP_208_ALREADY_REPORTED,
            "The user is already a collaborator of the course",
        )


class IsNotACollaborator(CourseException):
    def __init__(self, courseName):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            f"The user is not a collaborator of the course '{courseName}'",
        )


class UserNotFound(CourseException):
    def __init__(self):
        super().__init__(status.HTTP_404_NOT_FOUND, "User not found")


class IsAlreadySubscribed(CourseException):
    def __init__(self):
        super().__init__(
            status.HTTP_208_ALREADY_REPORTED, "You are already subscribed to the course"
        )


class IsNotSubscribed(CourseException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND, "You are not subscribed to the course"
        )


class SubscriptionInvalid(CourseException):
    def __init__(self):
        super().__init__(
            status.HTTP_403_FORBIDDEN,
            "You should upgrade your membership to enroll this course",
        )


class UserBlocked(CourseException):
    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            "Your account is blocked",
        )


class InvalidSubscriptionType(CourseException):
    def __init__(self, subscriptionTypes):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            f"The subscription must be of one of the "
            f"following types: {', '.join(subscriptionTypes)} ",
        )


class InvalidStatusType(CourseException):
    def __init__(self, statusTypes):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            f"The status must be of one of the "
            f"following types: {', '.join(statusTypes)} ",
        )


class CourseIsAlreadyBlocked(CourseException):
    def __init__(self):
        super().__init__(
            status.HTTP_208_ALREADY_REPORTED,
            "The course is already blocked",
        )


class CourseIsNotBlocked(CourseException):
    def __init__(self):
        super().__init__(
            status.HTTP_208_ALREADY_REPORTED,
            "The course is not blocked",
        )


class CourseIsAlreadyLiked(CourseException):
    def __init__(self):
        super().__init__(
            status.HTTP_208_ALREADY_REPORTED,
            "The course is already liked",
        )


class CourseIsNotLiked(CourseException):
    def __init__(self):
        super().__init__(
            status.HTTP_208_ALREADY_REPORTED,
            "The course is not liked",
        )
