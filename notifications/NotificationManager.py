from typing import List
from exponent_server_sdk import PushClient, PushMessage
from external.users import Users
import json
# import firebase_admin
# from firebase_admin import credentials, messaging

# cred = credentials.Certificate("notifications/uba-demy-firebase-adminsdk-9gjwi-151171f2c4.json")
# firebase_admin.initialize_app(cred)


class NotificationManager:
    # def __init__(self, usersClient: Users):
    #     self.usersClient = usersClient

    # title: str, body: str, tokens: List[str], dataObject=None
    def sendNotification(self, collabRequest):
        dataObject = {"id_course": 1}
        response = PushClient().publish(
            PushMessage(to="ExponentPushToken[oOnm2SAFR3TXmiVrGuzUit]",
                        title="Queres colaborar?",
                        body="Hola queres colaborar en este curso?",
                        data=dataObject,
                        category="collaborations"))
        return response

    # def courseCancelled(self, courseName: str, usersToNotify: List[int]):
    #     title = "Course Cancelled"
    #     body = f"The course {courseName} was cancelled"
    #     tokens = self.getTokens(usersToNotify)
    #     self.sendNotification(title, body, tokens)
    #
    # def collaborationRequest(self, courseData: dict, collaboratorData: dict):
    #     title = "Collaboration Request"
    #     body = f"Hi {courseData['first_name']}, do you want to be a collaborator in {courseData['name']}?"
    #     token = self.getToken(collaboratorData["user_id"])
    #     return False
    #
    # def getTokens(self, userIds):
    #     return self.usersClient.getBatchUsers(userIds)
    #
    # def getToken(self, userId):
    #     return self.usersClient.getUser(userId)


# Cantidad de dinero que el curso recaudo en base a los suscriptores.
# CATEGORIA * numUsuarios / 100, caja de ahorro.
