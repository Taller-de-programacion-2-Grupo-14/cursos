from typing import List
from exponent_server_sdk import PushClient, PushMessage

COLLAB_CATEGORY = "collaborations"


class NotificationManager:
    def sendNotification(self, receiver, title, body, extraData=None, categoryId=None):
        response = PushClient().publish(
            PushMessage(
                to=receiver, title=title, body=body, data=extraData, category=categoryId
            )
        )
        return response

    def courseCancelled(self, body: str, usersToNotify: List[str]):
        return self.sendNotification(usersToNotify, "Curso cancelado", body)

    def collaborationRequest(self, userToNotify: str, courseId: int, body: str):
        return self.sendNotification(
            userToNotify,
            "Solicitud de colaboracion",
            body,
            {"id_course": courseId},
            COLLAB_CATEGORY,
        )

    def courseFinished(self, userToNotify: str, courseName: str, courseStatus: str):
        courseStatus = "aprobaste" if courseStatus == "approved" else "desaprobaste"
        body = (
            f"Hola, {courseStatus} el curso '{courseName}'. "
            f"Para ver toda la informacion dirigete a la seccion 'Historico de cursos'"
        )
        self.sendNotification(userToNotify, "Curso finalizado", body)
