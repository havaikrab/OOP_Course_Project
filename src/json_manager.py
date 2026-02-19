import json
from typing import Optional

from src.base_manager import BaseManager
from src.utils import format_filename
from src.vacancy import Vacancy


class JSONManager(BaseManager):
    """Класс работы с JSON-файлами"""

    def __init__(self, filename: str, encoding: Optional[str] = "utf-8"):
        """Метод инициализации объекта класса. Принимает строку с именем файла, который будет определен, как база
        данных класса, и, опционально, строку с названием формата преобразования юникода"""

        self.__filename = format_filename(filename)
        self.__encoding = encoding
        self.__saved_id: set = set()

    def write_data(self, some_data: list[Vacancy]) -> None:
        """Абстрактный метод записи информации в файл"""

        with open(self.__filename, "w", encoding=self.__encoding) as file:
            json.dump(some_data, file, ensure_ascii=False, indent=4)

    def read_data(self) -> list:
        """Абстрактный метод получения информации из файла"""

        try:
            with open(self.__filename, "r", encoding=self.__encoding) as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                else:
                    raise ValueError("Файл базы данных поврежден")
        except FileNotFoundError:
            return list()

    def clear_data(self) -> None:
        """Абстрактный метод удаления всей информации из файла"""

        self.__saved_id = set()
        with open(self.__filename, "w", encoding=self.__encoding) as file:
            json.dump([], file)

    def __get_saved_id(self) -> None:
        """Приватный метод, возвращающий множество строк соответствующих оригинальному номеру вакансии,
        размещенной на сайте hh.ru"""

        self.__saved_id = set()
        data = self.read_data()
        for item in data:
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

    def update(self, vacancies_list: list[Vacancy]) -> None:
        """Метод обновления базы данных класса передаваемым списком вакансий"""

        current_data = self.read_data()
        vacancies_list = self.__exclude_duplicates(vacancies_list)
        for vacancy in vacancies_list:
            current_data.append(vacancy.to_dict())
        self.write_data(current_data)
