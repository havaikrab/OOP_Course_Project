import json
import os

import requests
from requests.exceptions import ConnectionError


def get_area_code() -> dict:
    """Возвращает словарь всех доступных кодов городов, регионов, стран,
    предоставляющих рабочие вакансии на сайте HH.ru"""

    location_code = dict()
    try:
        response = requests.get("https://api.hh.ru/areas/")
    except ConnectionError:
        print("Отсутствует подключение к сети")
    else:
        if response.status_code == 200:
            for i in response.json():
                regions = dict()
                for j in i.get("areas"):
                    cities = dict()
                    for k in j.get("areas"):
                        cities[k.get("name").lower()] = int(k.get("id"))
                    regions[j.get("name").lower()] = {"id": int(j.get("id")), "cities": cities}
                location_code[i.get("name").lower()] = {"id": int(i.get("id")), "regions": regions}
    finally:
        return location_code


def format_filename(path_to_file: str) -> str:
    """Принимает строку с именем файла вместе с путем к нему. Создает указанную директорию и возвращает форматированную
    строку с названием файла"""

    path_to_file = path_to_file.replace("/", "\\").strip("\\")
    if "\\" in path_to_file:
        directory_list = path_to_file.split("\\")
        directory = "\\".join(directory_list[:-1])
        os.makedirs(directory, exist_ok=True)
    return path_to_file


def write_area_codes_to_file(area_codes: dict) -> None:
    """Перезаписывает словарь с кодами стран, регионов, городов в файл data/area_codes.json"""

    if area_codes != dict():
        with open("data/area_codes.json", "w", encoding="utf-8") as file:
            json.dump(area_codes, file, indent=4, ensure_ascii=False)
