import os
import requests


class Users:
    def __init__(self):
        self.host = os.environ.get("USERS_HOSTNAME")

    def getUser(self, userId: int):
        response = requests.get(f"{self.host}users?id={userId}")
        response.raise_for_status()
        return response.json()

    def getBatchUsers(self, userIds: list):
        if not userIds:
            return {}
        response = requests.get(f"{self.host}users/batch?ids={','.join(map(str, userIds))}")
        response.raise_for_status()
        return response.json()
