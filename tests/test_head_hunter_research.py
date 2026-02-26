from typing import Any
from unittest.mock import patch

from requests.exceptions import ConnectionError

from src.head_hunter_research import HHResearch
from src.salary import Salary


def test_hhr_init() -> None:
    hhr_object = HHResearch(text="Разработчик", area=123)
    assert hhr_object.status_code is None
    assert hhr_object.response == list()


@patch("requests.head")
def test_get_response_no_connect(mock_head: Any) -> None:

    mock_head.side_effect = ConnectionError
    hhr_object = HHResearch(text="Разработчик", area=123)
    assert hhr_object.status_code is None
    assert hhr_object.response == list()
    assert mock_head.call_count == 0

    hhr_object.get_response()
    assert hhr_object.status_code is None
    assert hhr_object.response == list()
    assert mock_head.call_count == 20


@patch("requests.head")
def test_get_response_bad_response(mock_head: Any) -> None:

    mock_head.return_value.status_code = 500
    hhr_object = HHResearch(text="Разработчик", area=123)
    assert hhr_object.response == list()

    hhr_object.get_response()
    assert hhr_object.status_code == 500
    assert hhr_object.response == list()
    assert mock_head.call_count == 20


@patch("requests.head")
@patch("requests.get")
def test_get_response(mock_get: Any, mock_head: Any) -> None:

    Salary.required_currency = "RUB"
    Salary.currency_rates = None

    mock_head.return_value.status_code = 200
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "Something": "Useless",
        "items": [
            {
                "id": "111",
                "name": "Работник",
                "area": {"id": "1", "name": "Россия"},
                "salary": {"from": 1000, "currency": "EUR", "gross": False},
                "created_at": None,
                "employer": {},
                "alternate_url": "https://hh.ru/vacancy/111",
                "salary_range": {
                    "from": 1000,
                    "to": 2000,
                    "currency": "EUR",
                    "mode": {"name": "За месяц"},
                },
            },
            {
                "id": "222",
                "name": "Бездельник",
                "created_at": "Давно",
                "salary_range": {},
                "alternate_url": None,
            },
            {
                "id": "333",
                "name": "Директор",
                "created_at": "2026-02-02T08:00:00+0300",
                "alternate_url": "https://hh.ru/vacancy/333",
                "salary_range": {"from": 5000, "to": 6000, "currency": "EUR", "mode": {"name": "За месяц"}},
            },
        ],
    }
    hh_request = HHResearch()
    vacancies_list = hh_request.get_response()
    assert len(vacancies_list) == 40
    assert vacancies_list[0] == vacancies_list[2]
    assert vacancies_list[1] == vacancies_list[3]
    assert mock_get.call_count == 20
    assert hh_request.status_code == 200

    Salary.required_currency = None
    Salary.currency_rates = None
