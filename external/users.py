import os

import requests


class Users:
    def __init__(self):
        self.host = os.environ.get('USERS_HOSTNAME')

    def getUser(self, userId: int):
        response = requests.get(f"{self.host}users?id={userId}")
        response.raise_for_status()
        return response.json()

    def getBatchUsers(self, ids: list):
        if not ids:
            return {}
        response = requests.get(f"{self.host}users/batch?ids={','.join(map(str, ids))}")
        response.raise_for_status()
        return response.json()
