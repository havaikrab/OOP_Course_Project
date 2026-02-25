import os
from typing import Any, Optional
from unittest.mock import patch

import pytest

from src.salary import Salary


def test_salary_init(test_salary_dict: dict) -> None:

    some_salary = Salary(Salary.reform_original(test_salary_dict))
    assert some_salary.amount_from == 270000
    assert some_salary.amount_to == 300000
    assert some_salary.currency == "RUB"
    assert some_salary.converted_from == 0
    assert some_salary.converted_to is None
    assert str(some_salary) == " от 270000 до 300000 RUB за месяц"
    assert some_salary.converted_salary() == "Валюта для конвертации не определена"


def test_unspecific_init() -> None:

    some_salary = Salary(Salary.reform_original({"currency": "EUR", "mode": {"id": "MONTH", "name": "За месяц"}}))
    assert some_salary.amount_from == 0
    assert some_salary.amount_to is None
    assert some_salary.currency == "EUR"
    assert some_salary.converted_from == 0
    assert some_salary.converted_to is None
    assert str(some_salary) == " EUR за месяц"


@pytest.mark.parametrize(
    "salary_dict",
    [
        ({}),
        ({"from": 270000, "to": 300000, "gross": False, "mode": {"id": "MONTH", "name": "За месяц"}}),
        ({"from": 270000, "to": 300000, "gross": False, "currency": "USD", "mode": {"id": "MONTH"}}),
        (
            {
                "from": "270000",
                "to": 300000,
                "gross": False,
                "currency": "USD",
                "mode": {"id": "MONTH", "name": "За месяц"},
            }
        ),
        (
            {
                "from": 270000,
                "to": "300000",
                "gross": False,
                "currency": "USD",
                "mode": {"id": "MONTH", "name": "За месяц"},
            }
        ),
    ],
)
def test_invalid_init(salary_dict: dict) -> None:
    with pytest.raises(ValueError):
        Salary(Salary.reform_original(salary_dict))


@patch("time.time")
@patch("requests.get")
def test_set_currency_rates(mock_get: Any, mock_time: Any, test_salary_dict: dict) -> None:
    mock_time.return_value = 1771004000
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "quotes": {"USDEUR": 0.84, "USDRUB": 75.0},
        "source": "USD",
        "timestamp": 1771000000,
    }
    some_salary = Salary(Salary.reform_original(test_salary_dict))
    assert some_salary.currency_rates is None

    Salary.set_currency_rates("USD", file_name="test_data/test_rates.json")
    assert Salary.required_currency == "USD"

    other_salary = Salary(Salary.reform_original(test_salary_dict))
    assert some_salary.converted_from == 0.0
    assert some_salary.converted_to is None

    assert other_salary.converted_from == 3600.0
    assert other_salary.converted_to == 4000.0

    Salary.currency_rates = None
    Salary.required_currency = None
    os.remove("test_data/test_rates.json")


@pytest.mark.parametrize("bottom, top", [(100, 500), (0, None), (300, None)])
def test_magic_eq(bottom: int, top: Optional[int], test_salary_dict: dict) -> None:

    some_salary = Salary(Salary.reform_original(test_salary_dict))
    some_salary.converted_from = bottom
    some_salary.converted_to = top

    other_salary = Salary(Salary.reform_original(test_salary_dict))
    other_salary.converted_from = bottom
    other_salary.converted_to = top

    assert some_salary == other_salary


def test_false_magic_eq(test_salary_dict: dict) -> None:

    Salary.set_currency_rates("RUB")

    some_salary = Salary(Salary.reform_original(test_salary_dict))
    some_salary.converted_from = 300
    some_salary.converted_to = None

    other_salary = Salary(Salary.reform_original(test_salary_dict))
    other_salary.converted_from = 300

    assert some_salary != other_salary

    Salary.required_currency = None
    Salary.currency_rates = None


def test_incorrect_eq(test_salary_dict: dict) -> None:

    some_salary = Salary(Salary.reform_original(test_salary_dict))
    with pytest.raises(TypeError):
        some_salary == 123  # type: ignore


@pytest.mark.parametrize(
    "self_from, self_to, other_from, other_to",
    [
        (100, 500, 0, 500),
        (0, 300, 299, 299),
        (0, 300, 299, None),
        (300, None, 300, 300),
        (301, None, 0, 300),
        (300, None, 200, None),
    ],
)
def test_magic_lt(
    self_from: int, self_to: Optional[int], other_from: int, other_to: Optional[int], test_salary_dict: dict
) -> None:

    some_salary = Salary(Salary.reform_original(test_salary_dict))
    some_salary.converted_from = self_from
    some_salary.converted_to = self_to

    other_salary = Salary(Salary.reform_original(test_salary_dict))
    other_salary.converted_from = other_from
    other_salary.converted_to = other_to

    assert some_salary > other_salary


def test_limit_magic_lt(test_salary_dict: dict) -> None:

    some_salary = Salary(Salary.reform_original(test_salary_dict))
    some_salary.converted_from = 300
    some_salary.converted_to = None

    other_salary = Salary(Salary.reform_original(test_salary_dict))
    other_salary.converted_from = 100
    other_salary.converted_to = 300

    assert not some_salary < other_salary


def test_incorrect_lt(test_salary_dict: dict) -> None:

    some_salary = Salary(Salary.reform_original(test_salary_dict))
    with pytest.raises(TypeError):
        some_salary < 123  # type: ignore


def test_validation(test_salary_dict: dict) -> None:

    some_salary = Salary(Salary.reform_original(test_salary_dict))
    some_salary.mode = "За неделю"
    other_salary = Salary(Salary.reform_original(test_salary_dict))
    other_salary.mode = "За месяц"
    with pytest.raises(ValueError):
        assert some_salary == other_salary


def test_salary_to_dict(test_salary_dict: dict) -> None:

    Salary.set_currency_rates("RUB")

    some_salary = Salary(Salary.reform_original(test_salary_dict))
    assert some_salary.to_dict() == {
        "amount_from": 270000,
        "amount_to": 300000,
        "currency": "RUB",
        "mode": "За месяц",
        "converted_from": 270000,
        "converted_to": 300000,
        "required_currency": "RUB",
    }

    Salary.required_currency = None
    Salary.currency_rates = None
