import pytest

from src.json_manager import JSONManager
from src.vacancy import Vacancy


def test_json_manager_read_clear_update_data(
    parsed_vacancy_dict: dict, test_vacancy_dict: dict, test_other_vacancy_dict: dict
) -> None:

    first_vacancy = Vacancy(parsed_vacancy_dict)
    second_vacancy = Vacancy(Vacancy.reform_original(test_vacancy_dict))
    third_vacancy = Vacancy(Vacancy.reform_original(test_other_vacancy_dict))
    third_vacancy.salary = None
    vacancies_list = [first_vacancy, second_vacancy, third_vacancy]
    some_manager = JSONManager("test_data/some_test_data.json")
    some_manager.clear_data()
    assert some_manager.read_data() == list()

    some_manager.update_data(vacancies_list)
    current_data = some_manager.read_data()
    assert len(current_data) == 2
    assert Vacancy(current_data[0]) == first_vacancy
    assert Vacancy(current_data[1]) == third_vacancy

    some_manager.update_data(vacancies_list)
    current_data = some_manager.read_data()
    assert len(current_data) == 2
    assert Vacancy(current_data[0]) == first_vacancy
    assert Vacancy(current_data[1]) == third_vacancy


def test_json_manager_read_missing_data() -> None:

    unused_manager = JSONManager("missing.unknown")
    assert unused_manager.read_data() == list()


def test_invalid_data_base() -> None:

    some_manager = JSONManager("test_data/some_test_data.json")
    some_manager.clear_data()
    some_manager.write_data({1: "one", 2: "two", 3: "three"})  # type: ignore
    with pytest.raises(ValueError):
        some_manager.read_data()
