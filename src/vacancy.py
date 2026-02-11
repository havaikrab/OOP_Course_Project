from src.salary import Salary


class Vacancy:
    """Класс отображения вакансий сайта hh.ru"""

    vacancies_count: int = 0

    __slots__ = (
        "_name",
        "_vacancy_link",
        "_salary",
        "_location",
        "_created_at",
        "_employer_name",
        "_employer_link",
        "_requirements",
        "_responsibility",
    )

    def __init__(self, vacancy_dict: dict):
        """Метод инициализации объекта класса Vacancy. В качестве аргумента принимает словарь, содержащий информацию о
        вакансии формата api.hh.ru. Поля создаваемого объекта:
        _name - название вакансии
        _vacancy_link - ссылка на оригинал вакансии, размещенной на сайте hh.ru
        _salary - зарплата вакансии
        _location - местоположение работодателя
        _created_at - дата и время создания вакансии
        _employer_name - название организации-работодателя
        _employer_link - ссылка на организацию-работодателя
        _requirements - выдержка из описания требований к потенциальному работнику
        _responsibility - выдержка из описания обязанностей потенциального работника
        """

        self_name, self_link = vacancy_dict.get("name"), vacancy_dict.get("alternate_url")
        if not isinstance(self_name, str) or not isinstance(self_link, str):
            raise TypeError("Некорректные данные для инициализации обязательных атрибутов")
        self._name = self_name
        self._vacancy_link = self_link
        self._salary = None
        if vacancy_dict.get("salary_range"):
            try:
                self._salary = Salary(vacancy_dict["salary_range"])
            except ValueError:
                self._salary = None
        self._location = vacancy_dict.get("area", {}).get("name")
        self._created_at = vacancy_dict.get("created_at")
        self._employer_name = vacancy_dict.get("employer", {}).get("name")
        self._employer_link = vacancy_dict.get("employer", {}).get("alternate_url")
        self._requirements = vacancy_dict.get("snippet", {}).get("requirement")
        self._responsibility = vacancy_dict.get("snippet", {}).get("responsibility")
        Vacancy.vacancies_count += 1

    def __str__(self) -> str:
        """Метод предоставления краткого описания вакансии в виде строки"""

        result_str: str = self._name
        if self._salary:
            result_str += f". Зарплата{self._salary}"
        else:
            result_str += ". Зарплата не указана"
        return result_str + f". {self._vacancy_link}"

    @classmethod
    def __validate(cls, something: object) -> "Vacancy":
        """Метод проверки, принадлежит ли объект к классу Vacancy"""

        if isinstance(something, Vacancy):
            return something
        raise TypeError("Объект не принадлежит к классу Vacancy")

    def __eq__(self, other: object) -> bool:
        """Метод сравнения вакансий по размеру зарплаты"""

        other = Vacancy.__validate(other)
        return self._salary == other._salary

    def __lt__(self, other: "Vacancy") -> bool:
        """Метод сравнения вакансий по размеру зарплаты"""

        other = Vacancy.__validate(other)
        if self._salary and other._salary:
            return self._salary < other._salary
        elif not self._salary and other._salary:
            return True
        return False

    def __le__(self, other: "Vacancy") -> bool:
        """Метод сравнения вакансий по размеру зарплаты"""

        other = Vacancy.__validate(other)
        if self._salary and other._salary:
            return self._salary <= other._salary
        elif not self._salary and other._salary:
            return True
        return False
