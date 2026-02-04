from typing import Any, Optional

import requests
from requests.exceptions import ConnectionError

from src.base_request import BaseRequest


class HHResearch(BaseRequest):
    """Класс get-запросов к сайту HH.ru"""

    __location_code: dict = {}
    status_code: int

    def __init__(self, text: Optional[str] = None, area: Optional[int] = None):
        """Метод инициализации параметров запроса списка вакансий с сайта HH.ru"""

        self.url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params: dict = {"page": 0, "per_page": 100, "text": text, "area": area}
        self.response: list = []

    @classmethod
    def get_area_code(cls) -> None:
        """Класс-метод получения всех доступных кодов городов, регионов, стран,
        предоставляющих рабочие вакансии на сайте HH.ru"""

        cls.__location_code = dict()
        try:
            response = requests.get("https://api.hh.ru/areas/")
        except ConnectionError:
            print("Отсутствует подключение к сети")
        else:
            cls.status_code = response.status_code
            if response.status_code == 200:
                for i in response.json():
                    regions = dict()
                    for j in i.get("areas"):
                        cities = dict()
                        for k in j.get("areas"):
                            cities[k.get("name").lower()] = int(k.get("id"))
                        regions[j.get("name").lower()] = {"id": int(j.get("id")), "cities": cities}
                    cls.__location_code[i.get("name").lower()] = {"id": int(i.get("id")), "regions": regions}

    def get_response(self) -> list[Any]:
        """Метод получения списка вакансий с сайта HH.ru"""

        self.response = list()
        while self.params["page"] != 20:
            try:
                response = requests.get(self.url, headers=self.headers, params=self.params)
            except ConnectionError:
                print("Отсутствует подключение к сети")
                break
            else:
                self.status_code = response.status_code
                if response.status_code == 200:
                    content = response.json()["items"]
                    for item in content:
                        self.response.append(item)
            self.params["page"] += 1
        self.params["page"] = 0
        return self.response

    @property
    def location_code(self) -> dict:
        """Геттер приватного атрибута __location_code, содержащего словарь с кодами городов, регионов, стран,
        предоставляющих рабочие вакансии на сайте HH.ru"""

        return self.__location_code
