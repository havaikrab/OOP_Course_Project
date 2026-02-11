from typing import Any, Optional
from unittest.mock import patch

import pytest

from src.currency_rate_revision import ApilayerRates
from src.salary import Salary


def test_salary_init(test_salary_dict: dict) -> None:

    some_salary = Salary(test_salary_dict)
    assert some_salary.bottom == 270000
    assert some_salary.top == 300000
    assert some_salary.currency == "RUB"
    assert some_salary.required_currency is None
    assert some_salary.converted_bottom == 0
    assert some_salary.converted_top is None
    assert str(some_salary) == " от 270000 до 300000 RUB за месяц"


def test_unspecific_init() -> None:

    some_salary = Salary({"currency": "EUR", "mode": {"id": "MONTH", "name": "За месяц"}})
    assert some_salary.bottom == 0
    assert some_salary.top is None
    assert some_salary.currency == "EUR"
    assert some_salary.required_currency is None
    assert some_salary.converted_bottom == 0
    assert some_salary.converted_top is None
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
        Salary(salary_dict)


def test_set_currency_rates(test_salary_dict: dict) -> None:

    some_salary = Salary(test_salary_dict)
    assert some_salary.currency_rates is None

    some_salary.set_currency_rates("USD")
    assert isinstance(some_salary.currency_rates, ApilayerRates)


@patch("requests.get")
def test_convert_salary(mock_get: Any, test_salary_dict: dict) -> None:
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "quotes": {"USDBRL": 5.225099, "USDEUR": 0.84601, "USDKGS": 87.450066, "USDKZT": 493.296182, "USDRUB": 80.0},
        "source": "USD",
        "success": True,
        "timestamp": 1770606968,
    }

    some_salary = Salary(test_salary_dict)
    some_salary.set_currency_rates("USD")
    some_salary.convert_salary()

    assert some_salary.required_currency == "USD"
    assert some_salary.converted_bottom == 3375.0
    assert some_salary.converted_top == 3750.0


def test_not_needed_convert_salary(test_salary_dict: dict) -> None:

    some_salary = Salary(test_salary_dict)
    some_salary.set_currency_rates("RUB")
    some_salary.convert_salary()

    assert some_salary.required_currency == "RUB"
    assert some_salary.converted_bottom == 270000
    assert some_salary.converted_top == 300000


@pytest.mark.parametrize("bottom, top", [(100, 500), (0, None), (300, None)])
def test_magic_eq(bottom: int, top: Optional[int], test_salary_dict: dict) -> None:

    some_salary = Salary(test_salary_dict)
    some_salary.converted_bottom = bottom
    some_salary.converted_top = top

    other_salary = Salary(test_salary_dict)
    other_salary.converted_bottom = bottom
    other_salary.converted_top = top

    assert some_salary == other_salary


def test_false_magic_eq(test_salary_dict: dict) -> None:

    some_salary = Salary(test_salary_dict)
    some_salary.converted_bottom = 300
    some_salary.converted_top = 500

    other_salary = Salary(test_salary_dict)
    other_salary.converted_bottom = 300

    assert some_salary != other_salary


def test_incorrect_eq(test_salary_dict: dict) -> None:

    some_salary = Salary(test_salary_dict)
    with pytest.raises(TypeError):
        some_salary == 123  # type: ignore


@pytest.mark.parametrize(
    "self_bottom, self_top, other_bottom, other_top",
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
    self_bottom: int, self_top: Optional[int], other_bottom: int, other_top: Optional[int], test_salary_dict: dict
) -> None:

    some_salary = Salary(test_salary_dict)
    some_salary.converted_bottom = self_bottom
    some_salary.converted_top = self_top

    other_salary = Salary(test_salary_dict)
    other_salary.converted_bottom = other_bottom
    other_salary.converted_top = other_top

    assert some_salary > other_salary


def test_limit_magic_lt(test_salary_dict: dict) -> None:

    some_salary = Salary(test_salary_dict)
    some_salary.converted_bottom = 300

    other_salary = Salary(test_salary_dict)
    other_salary.converted_bottom = 100
    other_salary.converted_top = 300

    assert not some_salary < other_salary


def test_incorrect_lt(test_salary_dict: dict) -> None:

    some_salary = Salary(test_salary_dict)
    with pytest.raises(TypeError):
        some_salary < 123  # type: ignore


@pytest.mark.parametrize(
    "self_mode, self_currency, other_mode, other_currency",
    [("За месяц", "USD", "За месяц", "RUB"), ("За месяц", "USD", "За неделю", "USD")],
)
def test_validation(
    self_mode: str, self_currency: str, other_mode: str, other_currency: str, test_salary_dict: dict
) -> None:

    some_salary = Salary(test_salary_dict)
    some_salary.required_currency = self_currency
    some_salary.mode = self_mode
    other_salary = Salary(test_salary_dict)
    other_salary.required_currency = other_currency
    other_salary.mode = other_mode
    with pytest.raises(ValueError):
        assert some_salary == other_salary
