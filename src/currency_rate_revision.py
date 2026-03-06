import json
import os
import time

import requests
from dotenv import load_dotenv
from requests.exceptions import ConnectionError

from src.base_request import BaseRequest


class ApilayerRates(BaseRequest):
    """Класс get-запросов к сайту apilayer.com для получения актуальных курсов валют"""

    def __init__(self, currency: str, filename: str = "data/currency_rates.json"):
        """Метод инициализации объекта класса, в качестве аргумента принимает строку с кодом валюты,
        относительно которой будут рассчитаны курсы всех остальных валют и, опционально, имя файла для временного
        хранения курсов валют"""

        self.currency = currency
        self.filename = filename
        self.status = "Устаревший"
        self.last_update: int = 0
        load_dotenv()
        self.headers = {"apikey": os.getenv("exchangerates_API_KEY")}
        self.params = {"source": self.currency}
        self.url = "https://api.apilayer.com/currency_data/live"
        self.rates: dict = dict()

    def __clean_rates(self) -> dict:
        """Приватный метод удаления устаревших сведений о курсах валют"""

        try:
            with open(self.filename, "r", encoding="utf_8") as file:
                data = json.load(file)
                return {k: v for k, v in data.items() if time.time() - v.get("last_update", 0) < 3600}
        except FileNotFoundError:
            return dict()

    def __read_rates(self) -> None:
        """Приватный метод, для получения курсов валют, временно сохраненных в файле"""

        rates = self.__clean_rates()
        for k, v in rates.items():
            if k == self.currency:
                self.last_update = v.get("last_update", 0)
                self.rates = v.get("rates", dict())
                self.status = "Актуальный"

    def __request_rates(self) -> None:
        """Приватный метод обновления сведений о курсах валют"""

        try:
            response = requests.get(self.url, headers=self.headers, params=self.params)
        except ConnectionError:
            self.status = "Дисконнект"
        else:
            if response.status_code == 200:
                rates = response.json().get("quotes", dict())
                for k, v in rates.items():
                    self.rates[k.replace(self.currency, "")] = v
                self.last_update = response.json().get("timestamp", 0)
                self.status = "Актуальный"
            else:
                self.status = "Не авторизован"

    def __update_rates(self) -> None:
        """Приватный метод записи сведений о курсах валют в файл"""

        current_rates = self.__clean_rates()
        current_rates[self.currency] = {"last_update": self.last_update, "rates": self.rates}
        if "/" in self.filename:
            directory_list = self.filename.split("/")
            directory = "/".join(directory_list[:-1])
            os.makedirs(directory, exist_ok=True)
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(current_rates, file, indent=4, ensure_ascii=False)

    def get_response(self) -> dict:
        """Метод получения актуальных курсов валют"""

        self.__read_rates()
        if time.time() - self.last_update > 3600:
            self.__request_rates()
        self.__update_rates()
        return self.rates

    def convert_amount(self, user_amount: int | float, user_currency: str) -> float:
        """Метод конвертации суммы определенной валюты в сумму валюты экземпляра класса"""

        converted_amount = 0.0
        self.get_response()
        if self.rates != dict():
            currency_rate = self.rates.get(user_currency)
            if currency_rate:
                converted_amount = round(user_amount / currency_rate, 2)
        return converted_amount
