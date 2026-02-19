from typing import Optional

import requests
from requests.exceptions import ConnectionError

from src.base_request import BaseRequest
from src.vacancy import Vacancy


class HHResearch(BaseRequest):
    """Класс get-запросов к сайту HH.ru"""

    def __init__(self, text: Optional[str] = None, per_page: int = 100, area: Optional[int] = None):
        """Метод инициализации параметров запроса списка вакансий с сайта HH.ru"""

        self._url = "https://api.hh.ru/vacancies"
        self._headers = {"User-Agent": "HH-User-Agent"}
        self._params: dict = {"page": 0, "per_page": per_page, "text": text, "area": area}
        self._response: list = list()
        self.__location_code: dict = dict()
        self._status_code: Optional[int] = None

    def __check_connect(self) -> bool:
        """Метод проверки доступа к api сайта hh.ru"""

        try:
            response = requests.head(self._url, headers=self._headers)
            self._status_code = response.status_code
            if response.status_code == 200:
                return True
        except ConnectionError:
            return False
        return False

    def get_response(self) -> list[Vacancy]:
        """Метод получения вакансий с сайта HH.ru. Возвращает список объектов класса Vacancy"""

        self._response = list()
        stop_request = 2000 // self._params["per_page"]
        while self._params["page"] != stop_request:
            if self.__check_connect():
                response = requests.get(self._url, headers=self._headers, params=self._params)
                content = response.json().get("items")
                for item in content:
                    try:
                        self._response.append(Vacancy(Vacancy.reform_original(item)))
                    except TypeError:
                        continue
            self._params["page"] += 1
        self._params["page"] = 0
        return self._response
