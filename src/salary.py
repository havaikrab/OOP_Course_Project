from typing import Optional

from src.currency_rate_revision import ApilayerRates


class Salary:
    """Класс отображения зарплаты вакансии"""

    currency_rates: Optional[ApilayerRates] = None
    required_currency: Optional[str] = None

    __slots__ = (
        "amount_from",
        "amount_to",
        "currency",
        "mode",
        "converted_from",
        "converted_to",
    )

    def __init__(self, salary_dict: dict):
        """Метод инициализации объекта класса Salary. В качестве аргумента принимает общий словарь, содержащий
        информацию о вакансии и зарплате. Поля создаваемого объекта:

        amount_from - нижняя граница уровня зарплаты
        amount_to - верхняя граница уровня зарплаты
        currency - код оригинальной валюты зарплаты
        mode - порядок начисления зарплаты
        converted_from - эквивалент нижней границы уровня зарплаты в валюте пользователя
        converted_to - эквивалент верхней границы уровня зарплаты в валюте пользователя
        """

        self.amount_from = 0.0
        self_from = salary_dict.get("amount_from")
        if self_from:
            if not isinstance(self_from, (int, float)):
                raise ValueError("Значение не является числом")
            else:
                self.amount_from = self_from
        self.amount_to = None
        self_to = salary_dict.get("amount_to")
        if self_to:
            if not isinstance(self_to, (int, float)):
                raise ValueError("Значение не является числом")
            else:
                self.amount_to = self_to
        self_currency = salary_dict.get("currency")
        self_mode = salary_dict.get("mode")
        if not isinstance(self_currency, str) or not isinstance(self_mode, str):
            raise ValueError("Некорректно указана валюта зарплаты или порядок начисления зарплаты")
        self.currency = self_currency
        self.mode = self_mode
        self.converted_from: float = 0.0
        self.converted_to: float | None = None
        if Salary.currency_rates:
            if Salary.required_currency != self.currency:
                self.converted_from = Salary.currency_rates.convert_amount(self.amount_from, self.currency)
                if self.amount_to and Salary.currency_rates.convert_amount(self.amount_to, self.currency) != 0:
                    self.converted_to = Salary.currency_rates.convert_amount(self.amount_to, self.currency)
            else:
                self.converted_from = self.amount_from
                self.converted_to = self.amount_to

    def __str__(self) -> str:
        """Метод предоставления краткой информации о зарплате, указанной в вакансии"""

        result_str = ""
        if self.amount_from != 0:
            result_str += f" от {self.amount_from}"
        if self.amount_to:
            result_str += f" до {self.amount_to}"
        result_str += f" {self.currency}"
        result_str += f" {self.mode.lower()}"
        return result_str

    def __validate_compare(self, somthing: object) -> "Salary":
        """Метод валидации объекта для сравнения экземпляром класса Salary"""

        if isinstance(somthing, Salary):
            if self.mode == somthing.mode:
                return somthing
            raise ValueError("Атрибут mode должны быть одинаковыми у сравниваемых экземпляров")
        raise TypeError("Объект не принадлежит к классу Salary")

    def __eq__(self, other: object) -> bool:
        """Метод сравнения зарплат"""

        other = self.__validate_compare(other)
        if self.converted_to and other.converted_to:
            return self.converted_from == other.converted_from and self.converted_to == other.converted_to
        elif not self.converted_to and not other.converted_to:
            return self.converted_from == other.converted_from
        return False

    def __lt__(self, other: "Salary") -> bool:
        """Метод сравнения зарплат"""

        other = self.__validate_compare(other)
        if self.converted_to and other.converted_to:
            if self.converted_to == other.converted_to:
                return self.converted_from < other.converted_from
            return self.converted_to < other.converted_to
        elif self.converted_to and not other.converted_to:
            if self.converted_to == other.converted_from:
                return True
            else:
                return self.converted_to < other.converted_from
        elif not self.converted_to and other.converted_to:
            if self.converted_from == other.converted_to:
                return False
            else:
                return self.converted_from < other.converted_to
        else:
            return self.converted_from < other.converted_from

    def __le__(self, other: "Salary") -> bool:
        """Метод сравнения зарплат"""

        other = self.__validate_compare(other)
        return self < other or self == other

    @staticmethod
    def reform_original(salary_dict: dict) -> dict:
        """Статический метод для преобразования передаваемого словаря в словарь с ключами, необходимыми для создания
        нового объекта класса"""

        result = dict()
        mode_ = None
        mode_dict = salary_dict.get("mode")
        if isinstance(mode_dict, dict):
            mode_str = mode_dict.get("name")
            if isinstance(mode_str, str):
                mode_ = mode_str.replace("\xa0", " ")
        result["mode"] = mode_
        currency_ = salary_dict.get("currency")
        if currency_ == "RUR":
            currency_ = "RUB"
        result["currency"] = currency_
        result["amount_from"] = salary_dict.get("from")
        result["amount_to"] = salary_dict.get("to")
        return result

    @classmethod
    def set_currency_rates(cls, user_currency: str, file_name: str = "data/currency_rates.json") -> None:
        """Класс-метод, присваивающий атрибуту currency_rates объект класса ApilayerRates для переданной валюты,
        вызвав у которого метод get_response() можно получить словарь с курсами всех доступных на сайте apilayer.com
        валют относительно переданной"""

        cls.currency_rates = ApilayerRates(user_currency, filename=file_name)
        cls.required_currency = user_currency

    def to_dict(self) -> dict:
        """Метод преобразования объекта класса Salary в словарь, в котором элементами являются названия атрибутов,
        указанных в __slots__ с соответствующими им значениями"""

        result = {slot: getattr(self, slot, None) for slot in self.__slots__}
        result["required_currency"] = Salary.required_currency
        return result

    def converted_salary(self) -> str:
        """Метод предоставления краткой информации о зарплате в валюте класса,
        указанной в атрибуте required_currency"""

        if Salary.required_currency:
            result_str = ""
            if self.converted_from != 0:
                result_str += f" от {self.converted_from}"
            if self.converted_to:
                result_str += f" до {self.converted_to}"
            result_str += f" {Salary.required_currency}"
            result_str += f" {self.mode.lower()}"
            return result_str
        return "Валюта для конвертации не определена"
