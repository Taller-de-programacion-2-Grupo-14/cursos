import os
import requests


class Users:
    def __init__(self):
        self.host = os.environ.get('USERS_HOSTNAME')

    def getUser(self, userId: int):
        response = requests.get(f"{self.host}users?id={userId}")
        response.raise_for_status()
        return response.json()

    def getUserIdByName(self, userName: dict):
        firstName, lastName = userName.get("firstName", ""), userName.get("lastName")
        response = requests.get(f"{self.host}users?first_name={firstName}&last_name={lastName}")
        response.raise_for_status()
        return response.json()
