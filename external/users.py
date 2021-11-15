import os

import requests


class Users:
    def __init__(self):
        self.host = os.environ.get('USERS_HOSTNAME')

    def getUser(self, userId: int):
        response = requests.get(f"{self.host}users?id={userId}")
        response.raise_for_status()
        return response.json()
