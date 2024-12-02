import requests
import allure
from config import BASE_URL_API


class BaseApi:
    def __init__(self):
        self.base_url = BASE_URL_API
        self.session = requests.Session()

    @allure.step("API {method} request to {url}")
    def request(self, method, url, **kwargs):
        response = self.session.request(method, f"{self.base_url}{url}",verify=False, **kwargs)
        return response

