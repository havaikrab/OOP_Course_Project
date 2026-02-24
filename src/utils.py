import json
import os
from typing import Optional

import requests
from requests.exceptions import ConnectionError


def get_area_codes() -> dict:
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


def identify_country_code(country: str, guide: dict) -> tuple[int, dict]:
    """Принимает строку с названием страны, возвращает код, присвоенный сайтом hh.ru указанной стране"""

    for k, v in guide.items():
        if k == country.lower():
            return v.get("id"), v.get("regions")
    return 1001, guide.get("другие регионы", dict()).get("regions", dict())


def identify_region_code(region: str, guide: dict) -> tuple[int, dict]:
    """Принимает строку с названием региона, возвращает код, присвоенный сайтом hh.ru указанному региону"""

    for k, v in guide.items():
        if k == region:
            return v.get("id"), v.get("cities")
    return 0, dict()


def identify_city_code(city: str, guide: dict, region: Optional[str] = None) -> int:
    """Принимает строку с названием города, возвращает код, присвоенный сайтом hh.ru указанному городу"""

    for k, v in guide.items():
        if city == k and isinstance(v, int):
            return v
    if region:
        for k, v in guide.items():
            if city in k and region in k and isinstance(v, int):
                return v
    return 0


def area_code_detector() -> int | None:
    """Функция определяющая наиболее точный код страны, региона, города, присвоенный сайтом hh.ru,
    на основании введенных пользователем данных."""

    user_country = input("Введите название страны: ")
    country_tuple = identify_country_code(user_country.lower(), get_area_codes())
    current_code: int = country_tuple[0]
    if current_code == 1001:
        region_tuple = identify_region_code(user_country.lower(), country_tuple[1])
        if region_tuple[0] == 0:
            print(f'В источнике нет информации о вакансиях в "{user_country}".')
            return None
        else:
            current_code = region_tuple[0]
            if region_tuple[1] == dict():
                return current_code
            else:
                user_city = input("Введите название города: ")
                if identify_city_code(user_city.lower(), region_tuple[1]) == 0:
                    print(f'В источнике нет информации о вакансиях в "{user_city}".')
                    return current_code
                return identify_city_code(user_city.lower(), region_tuple[1])
    else:
        user_region = input("Введите название региона: ")
        region_tuple = identify_region_code(user_region.lower(), country_tuple[1])
        if region_tuple[1] == dict():
            if region_tuple[0] == 0:
                user_city = input("Введите название города: ")
                if identify_region_code(user_city.lower(), country_tuple[1])[0] == 0:
                    print(f'В источнике нет информации о вакансиях в "{user_city}".')
                    return current_code
                return identify_region_code(user_city.lower(), country_tuple[1])[0]
            return region_tuple[0]
        else:
            current_code = region_tuple[0]
            user_city = input("Введите название города: ")
            if identify_city_code(user_city.lower(), region_tuple[1], user_region.lower()) == 0:
                if identify_region_code(user_city.lower(), country_tuple[1])[0] == 0:
                    print(f'В источнике нет информации о вакансиях в "{user_city}".')
                    return current_code
                return identify_region_code(user_city.lower(), country_tuple[1])[0]
            return identify_city_code(user_city.lower(), region_tuple[1], user_region.lower())


def detect_inclusions(location: str) -> list:
    """Метод, определяющий список административно-территориальных субъектов, входящих в состав субъекта,
    в названии которого есть строка, переданная в качестве аргумента"""

    areas_dict = get_area_codes()
    areas_list = [location.lower()]
    for a, b in areas_dict.items():
        if location.lower() in a:
            areas_list.append(a)
            for c, d in b.get("regions").items():
                areas_list.append(c)
                areas_list.extend(list(d.get("cities", dict()).keys()))
        else:
            for i, j in b.get("regions").items():
                if location.lower() in i:
                    areas_list.append(i)
                    areas_list.extend(list(j.get("cities", dict()).keys()))
                else:
                    areas_list.extend([area for area in j.get("cities", dict()).keys() if location.lower() in area])
    return areas_list
