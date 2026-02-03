from typing import Any, Optional

import requests

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

        response = requests.get("https://api.hh.ru/areas/")
        cls.status_code = response.status_code
        cls.__location_code = dict()
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

        while self.params["page"] != 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            self.status_code = response.status_code
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


# qwert = HHResearch(text='разработчик', area=4)
# qwert.params['page'] = 18
# vac = qwert.get_response()
# qwert.get_area_code()
#
# with open('area.json', 'w', encoding='utf-8') as file:
#     json.dump(qwert.location_code, file, indent=4, ensure_ascii=False)
# with open('vacancy.json', 'w', encoding='utf-8') as file:
#     json.dump(vac, file, indent=4, ensure_ascii=False)
