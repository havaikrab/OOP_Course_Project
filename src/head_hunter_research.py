from typing import Optional

import requests
from requests.exceptions import ConnectionError

from src.base_request import BaseRequest
from src.vacancy import Vacancy


class HHResearch(BaseRequest):
    """Класс get-запросов к сайту HH.ru"""

    def __init__(self, text: Optional[str] = None, per_page: int = 100, area: Optional[int] = None):
        """Метод инициализации параметров запроса списка вакансий с сайта HH.ru"""

        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params: dict = {"page": 0, "per_page": per_page, "text": text, "area": area}
        self.__response: list = list()
        self.__status_code: Optional[int] = None

    def __check_connect(self) -> bool:
        """Метод проверки доступа к api сайта hh.ru"""

        try:
            response = requests.head(self.__url, headers=self.__headers)
            self.__status_code = response.status_code
            if response.status_code == 200:
                return True
        except ConnectionError:
            return False
        return False

    def get_response(self) -> list[Vacancy]:
        """Метод получения вакансий с сайта HH.ru. Возвращает список объектов класса Vacancy"""

        self.__response = list()
        stop_request = 2000 // self.__params["per_page"]
        while self.__params["page"] != stop_request:
            if self.__check_connect():
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                content = response.json().get("items")
                for item in content:
                    try:
                        self.__response.append(Vacancy(Vacancy.reform_original(item)))
                    except TypeError:
                        continue
            self.__params["page"] += 1
        self.__params["page"] = 0
        return self.__response

    @property
    def status_code(self) -> int | None:
        """Геттер приватного атрибута __status_code"""

        return self.__status_code

    @property
    def response(self) -> list:
        """Геттер приватного атрибута __response"""

        return self.__response
