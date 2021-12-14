import os
import requests


class Users:
    def __init__(self):
        self.host = os.environ.get("USERS_HOSTNAME")

    def getUser(self, userId):
        if isinstance(userId, str):
            queryParam = "email="
        else:
            queryParam = "id="
        response = requests.get(f"{self.host}users?{queryParam}{userId}")
        # f"https://ubademy-14-prod.herokuapp.com/users?id={userId}" For debugging
        response.raise_for_status()
        return response.json()

    def getBatchUsers(self, userIds: list):
        if not userIds:
            return {}
        response = requests.get(
            f"{self.host}users/batch?ids={','.join(map(str, userIds))}"
        )
        # response = requests.get(
        #     f"https://ubademy-14-prod.herokuapp.com/users/batch?ids={','.join(map(str, userIds))}"
        # )  # For debugging
        response.raise_for_status()
        return response.json()

    def getUserToken(self, userId: int):
        response = requests.get(
            f"{self.host}get-token/{userId}"
        )
        # f"https://ubademy-14-prod.herokuapp.com/users?id={userId}" For debugging
        response.raise_for_status()
        return response.json()
