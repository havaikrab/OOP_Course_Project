import json
import os
from typing import Any
from unittest.mock import patch

import pytest

from src.json_manager import JSONManager
from src.salary import Salary
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
    assert current_data[0] == first_vacancy
    assert current_data[1] == third_vacancy

    some_manager.update_data(vacancies_list)
    current_data = some_manager.read_data()
    assert len(current_data) == 2
    assert current_data[0] == first_vacancy
    assert current_data[1] == third_vacancy
    os.remove("test_data/some_test_data.json")


def test_json_manager_read_missing_data() -> None:

    unused_manager = JSONManager("missing.unknown")
    assert unused_manager.read_data() == list()


def test_invalid_data_base() -> None:

    some_manager = JSONManager("test_data/some_test_data.json")
    some_manager.clear_data()
    with open("test_data/some_test_data.json", "w", encoding="utf-8") as file:
        json.dump({1: "one", 2: "two", 3: "three"}, file)
    with pytest.raises(ValueError):
        some_manager.read_data()
    os.remove("test_data/some_test_data.json")


@patch("time.time")
@patch("requests.get")
def test_given_sort_by_salary(mock_get: Any, mock_time: Any, saved_vacancies_data: list) -> None:
    mock_time.return_value = 177000010
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "quotes": {"KZTBYR": 39.318135, "KZTRUB": 0.153974, "KZTUZS": 24.468357},
        "source": "KZT",
        "timestamp": 177000000,
    }
    Salary.set_currency_rates("KZT", file_name="test_data/test_rates.json")
    vacancies = [Vacancy(vacancy) for vacancy in saved_vacancies_data]
    with pytest.raises(ValueError):
        JSONManager.sort_by_salary(vacancies)

    filtered_by_mode_vacancies = JSONManager.filter_by_salary_mode("за МЕСЯЦ", vacancies)
    assert [vacancy.hh_id for vacancy in filtered_by_mode_vacancies] == [
        "130660306",
        "130467116",
        "130573247",
        "130543586",
        "130646930",
        "130620371",
        "130544536",
        "130153084",
    ]

    sorted_vacancies = JSONManager.sort_by_salary(filtered_by_mode_vacancies)
    rated_salaries = [
        f"от {i.salary.converted_from} до {i.salary.converted_to} {Salary.required_currency}" for i in sorted_vacancies
    ]
    assert [str(vacancy.salary) for vacancy in sorted_vacancies] == [
        " от 1600000 KZT за месяц",
        " до 190000 RUB за месяц",
        " от 1000000 до 1200000 KZT за месяц",
        " от 5000000 до 7000000 UZS за месяц",
        " от 6500000 UZS за месяц",
        " от 6000000 UZS за месяц",
        " от 100000 до 200000 KZT за месяц",
        " от 1200 BYR за месяц",
    ]

    assert rated_salaries == [
        "от 1600000 до None KZT",
        "от 0.0 до 1233974.57 KZT",
        "от 1000000 до 1200000 KZT",
        "от 204345.56 до 286083.78 KZT",
        "от 265649.22 до None KZT",
        "от 245214.67 до None KZT",
        "от 100000 до 200000 KZT",
        "от 30.52 до None KZT",
    ]

    Salary.currency_rates = None
    Salary.required_currency = None
    os.remove("test_data/test_rates.json")
