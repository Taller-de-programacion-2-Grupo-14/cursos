from sqlalchemy.orm import Session
from sqlalchemy import text
from models.courses import Courses
from models.colaborators import Colaborators
from models.enrolled import Enrolled

DEFAULT_OFFSET = 0
DEFAULT_LIMIT = 100


class DB:
    def __init__(self, engine):
        self.session = Session(engine)

    def addCourse(self, courseInfo):
        name = courseInfo["name"]
        exams = courseInfo["exams"]
        creator_id = courseInfo["user_id"]
        type = courseInfo["type"]
        subscription = courseInfo["subscription"]
        location = courseInfo["location"]
        description = courseInfo["description"]
        hashtags = courseInfo.get("hashtags", "")
        c = Courses(
            name=name,
            exams=exams,
            creator_id=creator_id,
            type=type,
            subscription=subscription,
            description=description,
            hashtags=hashtags,
            location=location,
            cancelled=0,
        )
        self.session.add(c)
        self.session.commit()

    def getCourse(self, courseId):
        course = self.session.query(Courses).get(courseId)
        if not course:
            return None
        dic_course = {
            "name": course.name,
            "exams": course.exams,
            "creator_id": course.creator_id,
            "type": course.type,
            "subscription": course.subscription,
            "description": course.description,
            "hashtags": course.hashtags,
            "location": course.location,
            "cancelled": course.cancelled,
        }
        # return course._asdict()  Why not?
        return dic_course

    def getCourses(self, courseFilters):
        query = self._buildQuery("courses", filters=courseFilters)
        return self._parseResult(self.session.execute(text(query)))

    def deleteCourse(self, deleteCourse):
        query = self._buildQuery("courses", "UPDATE", ["cancelled = 1"], filters={"id": deleteCourse["id"]})
        self.session.execute(text(query))
        self.session.commit()

    def editCourse(self, courseNewInfo):
        columns = [f"{column} = {newValue}" for column, newValue in courseNewInfo.items() if column != "id"]
        query = self._buildQuery("courses", "UPDATE", columns, filters={"id": courseNewInfo["id"]})
        self.session.execute(text(query))
        self.session.commit()

    def addCollaborator(self, collaborator):
        new_colab = Colaborators(
            id_colaborator=collaborator["user_id"], id_course=collaborator["id"]
        )
        self.session.add(new_colab)
        self.session.commit()

    def removeCollaborator(self, collaborator):
        colab = self.session.query(Colaborators).get(
            (collaborator["user_to_remove"], collaborator["id"])
        )
        self.session.delete(colab)
        self.session.commit()

    def getCourseUsers(self, courseId, getSubscribers=True):
        table = "enrolled" if getSubscribers else "colaborators"
        column = "id_student" if getSubscribers else "id_colaborator"
        query = self._buildQuery(table, columns=[column], filters={"id_course": courseId})
        return {record.id_colaborator for record in self.session.execute(text(query))}

    def addSubscriber(self, id_course, subscriber_id):
        enrollment = Enrolled(
            id_course=id_course, id_student=subscriber_id, status="on course"
        )
        self.session.add(enrollment)
        self.session.commit()

    def removeSubscriber(self, courseId, subscriberId):
        filters = {"id_course": courseId, "id_student": subscriberId}
        query = self._buildQuery("enrolled", "DELETE", filters=filters)
        self.session.execute(text(query))
        self.session.commit()

    def getMySubscriptions(self, user_id):
        query = f"SELECT * FROM (SELECT id_course AS courseId FROM enrolled WHERE id_student \
                = {user_id}) as studentCourses JOIN courses AS c ON c.id \
                = studentCourses.courseId"
        return self._parseResult(self.session.execute(text(query)))

    def getUsers(self, courseId, userFilters):
        getSubscribers = userFilters["subscribers"]
        table = "enrolled" if getSubscribers else "colaborators"
        column = "id_student" if getSubscribers else "id_colaborator"
        filters = {"id_course": courseId, "offset": userFilters.get("offset", DEFAULT_OFFSET), "limit": userFilters.get("limit", DEFAULT_LIMIT)}
        query = self._buildQuery(table, columns=[column], filters=filters)
        self._parseResult(self.session.execute(text(query)))
        return self._parseResult(self.session.execute(text(query)))

    def getMyCourses(self, userId):
        query = self._buildQuery("courses", filters={"creator_id": userId})
        return self._parseResult(self.session.execute(text(query)))

    def _buildQuery(self, tableName, operation="SELECT", columns=None, filters=None):
        operation = operation.upper()
        if columns is None:
            columns = ["*"]
        filtersQuery = ("WHERE " + self._buildFilterQuery(filters)) if filters is not None else ""
        if operation == "SELECT":
            return f"{operation} {', '.join(columns)} FROM {tableName} {filtersQuery}"
        if operation == "DELETE":
            return f"{operation} FROM {tableName} {filtersQuery}"
        if operation == "UPDATE":
            #ToDo: Agregar algo para que valide si el formato es el correcto (col = value)
            return f"{operation} {tableName} SET {', '.join(columns)} {filtersQuery}"
        if operation == "INSERT":
            return f"{operation} INTO {tableName} VALUES({', '.join(columns)}"


    def _buildFilterQuery(self, filters):
        filterQuery = ""
        for filterName, value in filters.items():
            if filterName == "OFFSET" or filterName == "LIMIT":
                continue  # A dict does not have an order, this instructions must be at the end of the query
            if filterQuery:
                filterQuery += " AND "
            if filterName == "free_text":
                filterQuery += f"name LIKE '%{value}%' OR description LIKE '%{value}%'"
            elif type(value) == str:
                filterQuery += f"{filterName} LIKE '%{value}%'"
            else:
                filterQuery += f"{filterName} = {value}"
        if "offset" in filters:
            filterQuery += f"OFFSET {filters['OFFSET']}"
        if "limit" in filters:
            filterQuery += f"LIMIT {filters['LIMIT']}"
        return filterQuery

    def _parseResult(self, result):
        courses = []
        if not result:
            return courses
        for r in result:
            courses.append(r._asdict())
        return courses
