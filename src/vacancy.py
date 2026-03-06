from typing import Optional

from src.salary import Salary


class Vacancy:
    """Класс отображения вакансий сайта hh.ru"""

    __slots__ = (
        "__hh_id",
        "__name",
        "__vacancy_link",
        "__salary",
        "__location",
        "__created_at",
        "__employer_name",
        "__employer_link",
        "__requirements",
        "__responsibility",
    )

    def __init__(self, vacancy_dict: dict):
        """Метод инициализации объекта класса Vacancy. В качестве аргумента принимает общий словарь, содержащий
        информацию о вакансии и зарплате. Поля создаваемого объекта:
        __hh_id - уникальный идентификационный номер вакансии, присвоенный сайтом hh.ru
        __name - название вакансии
        __vacancy_link - ссылка на оригинал вакансии, размещенной на сайте hh.ru
        __salary - зарплата вакансии
        __location - местоположение работодателя
        __created_at - дата и время создания вакансии
        __employer_name - название организации-работодателя
        __employer_link - ссылка на организацию-работодателя
        __requirements - выдержка из описания требований к потенциальному работнику
        __responsibility - выдержка из описания обязанностей потенциального работника
        """

        self_id, self_name, self_link = (
            vacancy_dict.get("hh_id"),
            vacancy_dict.get("name"),
            vacancy_dict.get("vacancy_link"),
        )
        if not isinstance(self_id, str) or not isinstance(self_name, str) or not isinstance(self_link, str):
            raise TypeError("Некорректные данные для инициализации обязательных атрибутов")
        self.__hh_id = self_id
        self.__name = self_name
        self.__vacancy_link = self_link
        self.__salary: Salary | None = None
        try:
            self.__salary = Salary(vacancy_dict)
        except ValueError:
            self.__salary = None
        self.__location = vacancy_dict.get("location")
        self.__created_at = vacancy_dict.get("created_at")
        self.__employer_name = vacancy_dict.get("employer_name")
        self.__employer_link = vacancy_dict.get("employer_link")
        self.__requirements = vacancy_dict.get("requirements")
        self.__responsibility = vacancy_dict.get("responsibility")

    def __str__(self) -> str:
        """Метод предоставления краткого описания вакансии в виде строки"""

        result_str: str = self.__name
        if self.__salary:
            result_str += f". Зарплата{self.__salary}"
        else:
            result_str += ". Зарплата не указана"
        return result_str + f". {self.__vacancy_link}"

    @classmethod
    def __validate(cls, something: object) -> "Vacancy":
        """Метод проверки, принадлежит ли объект к классу Vacancy"""

        if isinstance(something, Vacancy):
            return something
        raise TypeError("Объект не принадлежит к классу Vacancy")

    def __eq__(self, other: object) -> bool:
        """Метод сравнения вакансий по размеру зарплаты"""

        other = Vacancy.__validate(other)
        if self.__salary:
            if other.salary:
                return self.__salary == other.salary
            return False
        else:
            if not other.salary:
                return True
            return False

    def __lt__(self, other: "Vacancy") -> bool:
        """Метод сравнения вакансий по размеру зарплаты"""

        other = Vacancy.__validate(other)
        if self.__salary and other.salary:
            return self.__salary < other.salary
        elif not self.__salary and other.salary:
            return True
        return False

    def __le__(self, other: "Vacancy") -> bool:
        """Метод сравнения вакансий по размеру зарплаты"""

        other = Vacancy.__validate(other)
        if self.__salary and other.salary:
            return self.__salary <= other.salary
        elif not self.__salary and other.salary:
            return True
        return False

    @staticmethod
    def reform_original(vacancy_dict: dict) -> dict:
        """Статический метод для преобразования передаваемого словаря в словарь с ключами, необходимыми для создания
        нового объекта класса"""

        result = dict()
        result["hh_id"] = vacancy_dict.get("id")
        result["name"] = vacancy_dict.get("name")
        result["vacancy_link"] = vacancy_dict.get("alternate_url")
        result["location"] = vacancy_dict.get("area", {}).get("name")
        result["created_at"] = vacancy_dict.get("created_at")
        result["employer_name"] = vacancy_dict.get("employer", {}).get("name")
        result["employer_link"] = vacancy_dict.get("employer", {}).get("alternate_url")
        result["requirements"] = vacancy_dict.get("snippet", {}).get("requirement")
        result["responsibility"] = vacancy_dict.get("snippet", {}).get("responsibility")
        salary_dict = vacancy_dict.get("salary_range")
        if isinstance(salary_dict, dict):
            salary_dict = Salary.reform_original(salary_dict)
            result.update(salary_dict)
        return result

    @property
    def hh_id(self) -> str:
        """Геттер оригинального идентификатора вакансии на сайте hh.ru"""

        return self.__hh_id

    @property
    def name(self) -> str:
        """Геттер названия вакансии"""

        return self.__name

    @property
    def vacancy_link(self) -> str:
        """Геттер ссылки на вакансию"""

        return self.__vacancy_link

    @property
    def salary(self) -> Salary | None:
        """Геттер зарплаты вакансии"""

        return self.__salary

    @salary.setter
    def salary(self, new_salary: Optional[Salary] = None) -> None:
        """Сеттер зарплаты вакансии"""

        if new_salary and not isinstance(new_salary, Salary):
            raise TypeError(f"Атрибуту __salary не может быть присвоен объект класса {type(new_salary)}")
        self.__salary = new_salary

    @property
    def location(self) -> str | None:
        """Геттер местоположения вакансии"""

        return self.__location

    @property
    def created_at(self) -> str | None:
        """Геттер даты создания вакансии"""

        return self.__created_at

    @property
    def employer_name(self) -> str | None:
        """Геттер названия организации-работодателя"""

        return self.__employer_name

    @property
    def employer_link(self) -> str | None:
        """Геттер ссылки на организацию-работодателя"""

        return self.__employer_link

    @property
    def requirements(self) -> str | None:
        """Геттер требований к кандидату, описанных в вакансии"""

        return self.__requirements

    @property
    def responsibility(self) -> str | None:
        """Геттер обязанностей работника, описанных в вакансии"""

        return self.__responsibility

    def to_dict(self) -> dict:
        """Метод преобразования объекта класса Vacancy в словарь, в котором элементами являются названия атрибутов,
        указанных в __slots__ с соответствующими им значениями"""

        slots = [slot.strip("_") for slot in self.__slots__]
        result = {slot.strip("_"): getattr(self, slot, None) for slot in slots if slot != "salary"}
        if self.__salary:
            result.update(self.__salary.to_dict())
        return result
