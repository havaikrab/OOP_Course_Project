# Данный модуль не имеет отношения к функционалу проекта, он "тестирует" заглушки "pass" в абстрактных классах,
# с целью сохранения 100%-ного покрытия кода тестами. :))

from src.base_manager import BaseManager
from src.base_request import BaseRequest


class TestClass(BaseManager, BaseRequest):

    def clear_data(self) -> str:

        super().clear_data()  # type: ignore
        return "Очищает базу данных"

    def read_data(self) -> str:

        super().read_data()  # type: ignore
        return "Читает базу данных"

    def update_data(self, test_string: str) -> str:

        super().update_data(test_string)  # type: ignore
        return test_string

    def get_response(self) -> str:

        super().get_response()  # type: ignore
        return "Получает ответ"


def test_abstract_methods() -> None:

    test_class = TestClass()
    assert test_class.read_data() == "Читает базу данных"
    assert test_class.clear_data() == "Очищает базу данных"
    assert test_class.update_data("Обновляет базу данных") == "Обновляет базу данных"
    assert test_class.get_response() == "Получает ответ"
