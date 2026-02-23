from typing import Any
from unittest.mock import patch

import pytest
from requests.exceptions import ConnectionError

from src.filters import MixinFilter
from src.salary import Salary
from src.vacancy import Vacancy


def test_filter_by_name(saved_vacancies_data: list) -> None:

    vacancies = [Vacancy(vacancy) for vacancy in saved_vacancies_data]
    filtered_vacancies = MixinFilter.filter_by_name("ВоДиТеЛь", vacancies)

    assert [vacancy.hh_id for vacancy in filtered_vacancies] == ["130543586", "130646930"]


@patch("src.utils.get_area_codes")
def test_filter_by_location(mock_areas: Any, saved_vacancies_data: list, area_codes: dict) -> None:

    mock_areas.return_value = area_codes
    vacancies = [Vacancy(vacancy) for vacancy in saved_vacancies_data]
    filtered_vacancies = MixinFilter.filter_by_location("ЗаХСТаН", vacancies)

    assert [vacancy.hh_id for vacancy in filtered_vacancies] == ["130660306", "130573247", "130646930", "129915513"]
    mock_areas.assert_called_once_with()


@patch("requests.get")
def test_filter_by_location_no_connect(mock_get: Any, saved_vacancies_data: list) -> None:

    mock_get.side_effect = ConnectionError
    vacancies = [Vacancy(vacancy) for vacancy in saved_vacancies_data]
    filtered_vacancies = MixinFilter.filter_by_location("Аста", vacancies)

    assert [vacancy.hh_id for vacancy in filtered_vacancies] == ["130573247", "130646930"]
    mock_get.assert_called_once_with("https://api.hh.ru/areas/")


def test_filter_by_employer(saved_vacancies_data: list) -> None:
    vacancies = [Vacancy(vacancy) for vacancy in saved_vacancies_data]
    filtered_vacancies = MixinFilter.filter_by_employer("Яндекс", vacancies)

    assert [vacancy.hh_id for vacancy in filtered_vacancies] == ["130620371"]


def test_sort_by_date(saved_vacancies_data: list) -> None:
    vacancies = [Vacancy(vacancy) for vacancy in saved_vacancies_data]
    sorted_vacancies = MixinFilter.sort_by_date(vacancies, reverse=True)

    assert [vacancy.hh_id for vacancy in sorted_vacancies] == [
        "129915513",
        "130100999",
        "130153084",
        "130467116",
        "130543586",
        "130544536",
        "130573247",
        "130620371",
        "130646930",
        "130660306",
    ]


@patch("time.time")
@patch("requests.get")
def test_sort_by_salary(mock_get: Any, mock_time: Any, saved_vacancies_data: list) -> None:

    mock_time.return_value = 177000010
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "quotes": {
            "UZSBYR": 1.6,
            "UZSKZT": 0.04,
            "UZSRUB": 0.00625,
        },
        "source": "UZS",
        "timestamp": 177000000,
    }

    Salary.set_currency_rates("UZS")
    vacancies = [Vacancy(vacancy) for vacancy in saved_vacancies_data]
    with pytest.raises(ValueError):
        MixinFilter.sort_by_salary(vacancies)

    filtered_by_mode_vacancies = MixinFilter.filter_by_salary_mode("за МЕСЯЦ", vacancies)
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

    sorted_vacancies = MixinFilter.sort_by_salary(filtered_by_mode_vacancies, reverse=True)
    rated_salaries = [f"от {i.salary.converted_from} до {i.salary.converted_to} USZ" for i in sorted_vacancies]
    sorted_vacancies.append(Vacancy(saved_vacancies_data[-1]))
    assert [str(vacancy.salary) for vacancy in sorted_vacancies] == [
        " от 1600000 KZT за месяц",
        " до 190000 RUB за месяц",
        " от 1000000 до 1200000 KZT за месяц",
        " от 5000000 до 7000000 UZS за месяц",
        " от 6500000 UZS за месяц",
        " от 6000000 UZS за месяц",
        " от 100000 до 200000 KZT за месяц",
        " от 1200 BYR за месяц",
        "None",
    ]
    assert rated_salaries == [
        "от 40000000.0 до None USZ",
        "от 0.0 до 30400000.0 USZ",
        "от 25000000.0 до 30000000.0 USZ",
        "от 5000000 до 7000000 USZ",
        "от 6500000 до None USZ",
        "от 6000000 до None USZ",
        "от 2500000.0 до 5000000.0 USZ",
        "от 750.0 до None USZ",
    ]

    Salary.currency_rates = None
    Salary.required_currency = None


@patch("src.utils.get_area_codes")
def test_filter_by_currency(mock_areas: Any, saved_vacancies_data: list, area_codes: dict) -> None:

    mock_areas.return_value = area_codes
    vacancies = [Vacancy(vacancy) for vacancy in saved_vacancies_data]
    for vacancy in vacancies[:8]:
        if vacancy.salary:
            vacancy.salary.currency = "UZS"
    filtered_vacancies = MixinFilter.filter_by_salary_currency("UZS", vacancies)
    assert [vacancy.hh_id for vacancy in filtered_vacancies] == [
        "130660306",
        "130467116",
        "130573247",
        "130543586",
        "130646930",
        "130620371",
        "130544536",
        "129915513",
        "130153084",
    ]

    filtered_vacancies = MixinFilter.filter_by_location("Ташкент", filtered_vacancies)
    assert [vacancy.hh_id for vacancy in filtered_vacancies] == ["130467116", "130543586", "130153084"]

    top_vacancies = MixinFilter.get_top(2, filtered_vacancies)
    assert [vacancy.hh_id for vacancy in top_vacancies] == ["130467116", "130543586"]
