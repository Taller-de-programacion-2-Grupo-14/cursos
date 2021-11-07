from exceptions.CourseException import *


class DB:
    def __init__(self):
        self.db = {}
        self.collaboratorsDB = {}
        self.id = 1

    def addCourse(self, courseInfo):
        self.db[self.id] = courseInfo
        self.id += 1

    def getCourse(self, courseId):
        return self.db[courseId] if courseId in self.db else None

    def getCourses(self, courseFilters):
        courses = []
        for course in self.db.values():
            print(courseFilters)
            courses.append(course)
        return courses

    def deleteCourse(self, deleteCourse):
        del self.db[deleteCourse['course_id']]
        if deleteCourse['course_id'] in self.collaboratorsDB:
            del self.collaboratorsDB[deleteCourse['course_id']]

    def editCourse(self, courseNewInfo):
        self.db[courseNewInfo['course_id']] = courseNewInfo
        # No es tan asi, solo cierta info podemos modificar otra es fija

    def addCollaborator(self, collaborator):
        self.collaboratorsDB[collaborator['course_id']] = \
            self.collaboratorsDB.get(collaborator['course_id'], []) + [collaborator['user_id']]

    def removeCollaborator(self, collaborator):
        self.collaboratorsDB[collaborator['course_id']].remove(collaborator['user_to_remove'])

    def _courseExists(self, courseId):
        if courseId not in self.db:
            raise CourseDoesNotExist

    def _isTheCourseCreator(self, userId, courseId):
        return self.db[courseId]['user_id'] == userId

    def getCourseName(self, courseId):
        return self.db[courseId]['course_name']

    def getCourseCreator(self, courseId):
        return self.db[courseId]['user_id']

    def getCoursesCreatedBy(self, user_id):
        courses = []
        for course in self.db.values():
            if course['user_id'] == user_id:
                courses.append(course['course_name'])
        return courses

    def getCourseCollaborators(self, courseId):
        return self.collaboratorsDB[courseId] if courseId in self.collaboratorsDB else []
