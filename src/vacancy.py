from src.salary import Salary


class Vacancy:
    """Класс отображения вакансий сайта hh.ru"""

    __slots__ = (
        "_hh_id",
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
        """Метод инициализации объекта класса Vacancy. В качестве аргумента принимает общий словарь, содержащий
        информацию о вакансии и зарплате. Поля создаваемого объекта:
        _hh_id - уникальный идентификационный номер вакансии, присвоенный сайтом hh.ru
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

        self_id, self_name, self_link = (
            vacancy_dict.get("hh_id"),
            vacancy_dict.get("name"),
            vacancy_dict.get("vacancy_link"),
        )
        if not isinstance(self_id, str) or not isinstance(self_name, str) or not isinstance(self_link, str):
            raise TypeError("Некорректные данные для инициализации обязательных атрибутов")
        self._hh_id = self_id
        self._name = self_name
        self._vacancy_link = self_link
        self._salary: Salary | None = None
        try:
            self._salary = Salary(vacancy_dict)
        except ValueError:
            self._salary = None
        self._location = vacancy_dict.get("location")
        self._created_at = vacancy_dict.get("created_at")
        self._employer_name = vacancy_dict.get("employer_name")
        self._employer_link = vacancy_dict.get("employer_link")
        self._requirements = vacancy_dict.get("requirements")
        self._responsibility = vacancy_dict.get("responsibility")

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
        if self._salary:
            if other._salary:
                return self._salary == other._salary
            return False
        else:
            if not other._salary:
                return True
            return False

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

        return self._hh_id

    def to_dict(self) -> dict:
        """Метод преобразования объекта класса Vacancy в словарь, в котором элементами являются названия атрибутов,
        указанных в __slots__ с соответствующими им значениями"""

        result = {slot[1:]: getattr(self, slot, None) for slot in self.__slots__ if slot != "_salary"}
        if self._salary:
            result.update(self._salary.to_dict())
        return result
