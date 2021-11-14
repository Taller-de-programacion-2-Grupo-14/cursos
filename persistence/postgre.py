from sqlalchemy.orm import Session
from sqlalchemy import text
from models.courses import Courses
from models.colaborators import Colaborators


class DB:
    def __init__(self, engine):
        self.session = Session(engine)

    def addCourse(self, courseInfo):
        name = courseInfo["name"]
        exams = courseInfo["exams"]
        creator_id = courseInfo["creator_id"]
        type = courseInfo["type"]
        subscription = courseInfo["subscription"]
        location = courseInfo["subscription"]
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
            "creator_name": course.creator_id,
            "type": course.type,
            "subscription": course.subscription,
            "description": course.description,
            "hashtags": course.hashtags,
            "location": course.location,
        }
        return dic_course

    def getCourses(self, courseFilters):
        # TODO: ver donde poner el canedit
        offset = courseFilters["offset"]
        limit = courseFilters["limit"]
        where_clause = ""
        endings = f"offset {offset} limit {limit}"
        if len(courseFilters) > 2:
            where_clause = " WHERE"
            for k, v in courseFilters:
                if k == "offset" or k == "limit":
                    pass
                if k == "exams":
                    filter = f"{k} = {v}"
                else:
                    filter = f"{k} LIKE '%{v}%'"
                if where_clause != " WHERE":
                    where_clause += "AND"
                where_clause += filter
        query = f"SELECT * FROM courses {where_clause} {endings}"
        self.session.execute(text(query))

    def deleteCourse(self, deleteCourse):
        course_id = deleteCourse["course_id"]
        user_id = deleteCourse["user_id"]
        course = self.session.query(Colaborators).get((user_id, course_id))
        if not course:
            return None
        self.session.delete(course)
        self.session.commit()

    def editCourse(self, courseNewInfo):
        course_id = courseNewInfo["course_id"]
        course = self.session.query(Courses).get(course_id)
        if "name" in courseNewInfo:
            course.name = courseNewInfo["name"]
        if "type" in courseNewInfo:
            course.type = courseNewInfo["type"]
        if "location" in courseNewInfo:
            course.location = courseNewInfo["location"]
        if "description" in courseNewInfo:
            course.description = courseNewInfo["description"]
        if "hashtags" in courseNewInfo:
            course.hashtags = courseNewInfo["hashtags"]
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

    def getCoursesCreatedBy(self, user_id):
        courses_creator = self.session.query(Courses).filter(
            Courses.creator_id == user_id
        )
        if not courses_creator.first():
            return None
        courses = []
        for c in courses_creator:
            courses.append(c)
        return courses

    def getCourseCollaborators(self, courseId):
        colabs_course = self.session.query(Colaborators).filter(
            Colaborators.id_course == courseId
        )
        if not colabs_course.first():
            return None
        colaborators = []
        for c in colabs_course:
            colaborators.append(c.id_colaborator)
        return colaborators
