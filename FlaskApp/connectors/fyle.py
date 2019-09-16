import os
import requests

from fylesdk import FyleSDK


class FyleConnector:
    def __init__(self,  refresh_token):
        self.__base_url = os.environ.get("BASE_URL")
        self.__client_id = os.environ.get("CLIENT_ID")
        self.__client_secret = os.environ.get("CLIENT_SECRET")
        self.__refresh_token = refresh_token

        self.__connection = FyleSDK(
            base_url=self.__base_url,
            client_id=self.__client_id,
            client_secret=self.__client_secret,
            refresh_token=self.__refresh_token
        )

    def get_employee_details(self):
        employee_data = self.__connection.Employees.get_my_profile()
        return employee_data.get('data')
