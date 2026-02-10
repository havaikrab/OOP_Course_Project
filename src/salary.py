from typing import Optional

from src.currency_rate_revision import ApilayerRates


class Salary:
    """Класс отображения зарплаты вакансии"""

    currency_rates: Optional[ApilayerRates] = None

    __slots__ = (
        "bottom",
        "top",
        "currency",
        "mode",
        "required_currency",
        "converted_bottom",
        "converted_top",
    )

    def __init__(self, salary_dict: dict):
        """Метод инициализации объекта класса Salary. В качестве аргумента принимает словарь, содержащий информацию о
        зарплате вакансии формата api.hh.ru. Поля создаваемого объекта:

        bottom - нижняя граница уровня зарплаты
        top - верхняя граница уровня зарплаты
        currency - код оригинальной валюты зарплаты
        mode - порядок начисления зарплаты
        required_currency - код валюты, указанной пользователем, для представления размера зарплаты
        converted_bottom - эквивалент нижней границы уровня зарплаты в валюте пользователя
        converted_top - эквивалент верхней границы уровня зарплаты в валюте пользователя
        """

        if isinstance(salary_dict.get("mode", {}).get("name"), str) and isinstance(salary_dict.get("currency"), str):
            self.currency = salary_dict.get("currency")
            if self.currency == "RUR":
                self.currency = "RUB"
            self.mode = salary_dict.get("mode", {}).get("name")
            self.mode = self.mode.replace("\xa0", " ")
        else:
            raise ValueError("Некорректно указана валюта зарплаты или порядок начисления зарплаты")
        self_bottom = salary_dict.get("from")
        if self_bottom:
            if isinstance(self_bottom, (int, float)):
                self.bottom = self_bottom
            else:
                raise ValueError("Значение не является числом")
        else:
            self.bottom = 0
        if salary_dict.get("to") and not isinstance(salary_dict.get("to"), (int, float)):
            raise ValueError("Значение не является числом")
        self.top = salary_dict.get("to")
        self.required_currency: str | None = None
        self.converted_bottom: int | float = 0
        self.converted_top: int | float | None = None

    def __str__(self) -> str:
        """Метод предоставления краткой информации о зарплате, указанной в вакансии"""

        result_str = ""
        if self.bottom != 0:
            result_str += f" от {self.bottom}"
        if self.top:
            result_str += f" до {self.top}"
        if self.currency:
            result_str += f" {self.currency}"
        if self.mode:
            result_str += f" {self.mode.lower()}"
        return result_str

    def __eq__(self, other: object) -> bool:
        """Метод сравнения зарплат"""

        if isinstance(other, Salary):
            if self.converted_top and other.converted_top:
                return self.converted_bottom == other.converted_bottom and self.converted_top == other.converted_top
            elif not self.converted_top and not other.converted_top:
                return self.converted_bottom == other.converted_bottom
            return False
        raise TypeError("Объект не принадлежит к классу Salary")

    def __lt__(self, other: "Salary") -> bool:
        """Метод сравнения зарплат"""

        if isinstance(other, Salary):
            if self.converted_top and other.converted_top:
                if self.converted_top == other.converted_top:
                    return self.converted_bottom < other.converted_bottom
                else:
                    return self.converted_top < other.converted_top
            elif self.converted_top and not other.converted_top:
                if self.converted_top == other.converted_bottom:
                    return True
                else:
                    return self.converted_top < other.converted_bottom
            elif not self.converted_top and other.converted_top:
                if self.converted_bottom == other.converted_top:
                    return False
                else:
                    return self.converted_bottom < other.converted_top
            else:
                return self.converted_bottom < other.converted_bottom
        raise TypeError("Объект не принадлежит к классу Salary")

    @classmethod
    def set_currency_rates(cls, user_currency: str) -> None:
        """Класс-метод, присваивающий атрибуту currency_rates объект класса ApilayerRates для переданной валюты,
        вызвав у которого метод get_response() можно получить словарь с курсами всех доступных на сайте apilayer.com
        валют относительно переданной"""

        cls.currency_rates = ApilayerRates(user_currency)

    def convert_salary(self) -> None:
        """Метод, определяющий эквивалент размера зарплаты вакансии в валюте, указанной пользователем"""

        if isinstance(Salary.currency_rates, ApilayerRates):
            self.required_currency = Salary.currency_rates.currency
            if self.currency and self.currency != self.required_currency:
                currency_rate = Salary.currency_rates.get_response().get(self.currency)
                if currency_rate:
                    self.converted_bottom = round(self.bottom / currency_rate, 2)
                    if self.top:
                        self.converted_top = round(self.top / currency_rate, 2)
            else:
                self.converted_bottom = self.bottom
                self.converted_top = self.top
