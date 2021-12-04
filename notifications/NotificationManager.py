import firebase_admin
from firebase_admin import credentials, messaging
from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)
from requests.exceptions import ConnectionError, HTTPError

cred = credentials.Certificate("notifications/uba-demy-firebase-adminsdk-9gjwi-151171f2c4.json")
firebase_admin.initialize_app(cred)


class NotificationManager:
    def sendNotification(self, collaborationRequest, dataObject=None):
        # title = "Hola queres colaborar?"
        # msg = "Hola que tal tu como estas? dime si eres feliz"
        # # token = 'ExponentPushToken[4Jpw10MsWSfkd_ZyXvhdT3]'
        # token = 'oOnm2SAFR3TXmiVrGuzUit'
        # message = messaging.Message(
        #     notification=messaging.Notification(
        #         title=title,
        #         body=msg
        #     ),
        #     data=dataObject,
        #     token=token,
        # )
        # return messaging.send(message)
        response = PushClient().publish(
            PushMessage(to="ExponentPushToken[oOnm2SAFR3TXmiVrGuzUit]",
                        title="Queres colaborar forro?",
                        body="Hola que tal tu como estas? dime si eres feliz",
                        data=dataObject))
        return response
