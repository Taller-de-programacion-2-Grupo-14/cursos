import os
import requests


class Exams:
    def __init__(self):
        # ToDo: change for exams
        self.host = os.environ.get("USERS_HOSTNAME")

    def _getExams(self, userId, url):
        response = requests.request(
            method="get",
            url=url,
            data={"user_id": userId}
        )
        return response.json()

    def getExams(self, courseId, userId):
        return self._getExams(userId, f"{self.host}exams/{courseId}")

    def getGradesFrom(self, courseId, userId):
        return self._getExams(userId, f"{self.host}resolutions/{courseId}")
