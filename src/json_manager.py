import json
from typing import Optional

from src.base_manager import BaseManager
from src.filters import MixinFilter
from src.utils import format_filename
from src.vacancy import Vacancy


class JSONManager(BaseManager, MixinFilter):
    """Класс работы с JSON-файлами"""

    def __init__(self, filename: Optional[str]='data/vacancies.json', encoding: Optional[str] = "utf-8"):
        """Метод инициализации объекта класса. Принимает строку с именем файла, который будет определен, как база
        данных класса, и, опционально, строку с названием формата преобразования юникода"""

        self.__filename = format_filename(filename)
        self.__encoding = encoding
        self.__current_data = list()
        self.__saved_id: set = set()


    def __open_data(self) -> None:
        """Приватный метод, присваивающий атрибуту __current_data содержимое файла базы данных"""

        try:
            with open(self.__filename, "r", encoding=self.__encoding) as file:
                data = json.load(file)
                if isinstance(data, list):
                    self.__current_data = data
                else:
                    raise ValueError("Файл базы данных поврежден")
        except FileNotFoundError:
            self.__current_data = list()


    def read_data(self) -> list[Vacancy]:
        """Метод получения информации о вакансиях из файла базы данных"""

        self.__open_data()
        return [Vacancy(item) for item in self.__current_data]


    def clear_data(self) -> None:
        """Метод полной очистки файла базы данных"""

        self.__saved_id = set()
        with open(self.__filename, "w", encoding=self.__encoding) as file:
            json.dump([], file)


    def __write_data(self, some_data: list) -> None:
        """Приватный метод записи информации в файл"""

        with open(self.__filename, "w", encoding=self.__encoding) as file:
            json.dump(some_data, file, ensure_ascii=False, indent=4)


    def __get_saved_id(self) -> None:
        """Приватный метод, обновляющий значение атрибута __saved_id, хранящий множество строк, соответствующих
        оригинальным номерам вакансий, размещенных на сайте hh.ru"""

        self.__saved_id = set()
        self.__open_data()
        for item in self.__current_data:
            self.__saved_id.add(item.get("hh_id"))

    def __exclude_duplicates(self, vacancies_list: list[Vacancy]) -> list:
        """Приватный метод, проверяющий передаваемый список на наличие вакансий, уже сохраненных в базе данных класса.
        Возвращает список, содержащий только новые вакансии"""

        self.__get_saved_id()
        result = list()
        result_id_set: set = set()
        for vacancy in vacancies_list:
            if vacancy.hh_id not in self.__saved_id and vacancy.hh_id not in result_id_set:
                result_id_set.add(vacancy.hh_id)
                result.append(vacancy)
        return result

    def update_data(self, vacancies_list: list[Vacancy]) -> None:
        """Метод обновления базы данных класса передаваемым списком вакансий"""

        self.__open_data()
        vacancies_list = self.__exclude_duplicates(vacancies_list)
        for vacancy in vacancies_list:
            self.__current_data.append(vacancy.to_dict())
        self.__write_data(self.__current_data)
