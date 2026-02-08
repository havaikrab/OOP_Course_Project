import os
import time

import requests
from dotenv import load_dotenv
from requests.exceptions import ConnectionError

from src.base_request import BaseRequest


class ApilayerRates(BaseRequest):
    """Класс get-запросов к сайту apilayer.com для получения актуальных курсов валют"""

    def __init__(self, currency: str):
        """Метод инициализации объекта класса, в качестве аргумента принимает строку с кодом валюты,
        относительно которой будут рассчитаны курсы всех остальных валют"""

        self.currency = currency
        self.last_update = 0
        load_dotenv()
        self.headers = {"apikey": os.getenv("exchangerates_API_KEY")}
        self.params = {"source": self.currency}
        self.url = "https://api.apilayer.com/currency_data/live"
        self._rates: dict = dict()

    def get_response(self) -> dict:
        """Метод получения актуальных курсов валют"""

        if time.time() - self.last_update > 3600:
            try:
                response = requests.get(self.url, headers=self.headers, params=self.params)
            except ConnectionError:
                print("Отсутствует подключение к сети, курс валюты может быть устаревшим")
            else:
                if response.status_code == 200:
                    rates = response.json().get("quotes")
                    for k, v in rates.items():
                        self._rates[k.replace(self.currency, "")] = v
                    self.last_update = response.json().get("timestamp")
        return self._rates
