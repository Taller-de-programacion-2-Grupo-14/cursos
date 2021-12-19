import os
import requests


class Exams:
    def __init__(self):
        self.host = os.environ.get("EXAMS_HOSTNAME")

    def _getExams(self, userId, url):
        response = requests.request(
            method="get",
            url=url,
            json={"user_id": userId}
        )
        response.raise_for_status()
        return response.json().get("message")

    def getExams(self, courseId, userId):
        return self._getExams(userId, f"{self.host}exams/{courseId}")

    def getGradesFrom(self, courseId, userId):
        return self._getExams(userId, f"{self.host}resolutions/{courseId}")
