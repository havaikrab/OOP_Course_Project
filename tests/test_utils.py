from typing import Any
from unittest.mock import patch

import pytest
from requests.exceptions import ConnectionError

from src import utils


@patch("requests.get")
def test_get_area_codes(mock_get: Any) -> None:
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {
            "id": "113",
            "parent_id": None,
            "name": "Россия",
            "areas": [
                {
                    "id": "1620",
                    "parent_id": "113",
                    "name": "Республика Марий Эл",
                    "areas": [
                        {
                            "id": "4228",
                            "parent_id": "1620",
                            "name": "Виловатово",
                            "areas": [],
                            "utc_offset": "+03:00",
                            "lat": 56.176148,
                            "lng": 46.606034,
                        },
                        {
                            "id": "1621",
                            "parent_id": "1620",
                            "name": "Волжск",
                            "areas": [],
                            "utc_offset": "+03:00",
                            "lat": 55.866128,
                            "lng": 48.356478,
                        },
                    ],
                }
            ],
        },
        {
            "id": "40",
            "parent_id": None,
            "name": "Казахстан",
            "areas": [
                {
                    "id": "6251",
                    "parent_id": "40",
                    "name": "Абай",
                    "areas": [],
                    "utc_offset": "+05:00",
                    "lat": 49.38,
                    "lng": 72.51,
                },
                {
                    "id": "6782",
                    "parent_id": "40",
                    "name": "Айет",
                    "areas": [],
                    "utc_offset": "+05:00",
                    "lat": 52.835556,
                    "lng": 62.511944,
                },
            ],
        },
        {
            "id": "9",
            "parent_id": None,
            "name": "Азербайджан",
            "areas": [
                {"id": "2970", "parent_id": "9", "name": "Агдаш", "areas": [], "utc_offset": "+04:00"},
                {"id": "2966", "parent_id": "9", "name": "Агджабеди", "areas": [], "utc_offset": "+04:00"},
            ],
        },
    ]
    area_codes = utils.get_area_codes()
    assert area_codes == {
        "россия": {
            "id": 113,
            "regions": {"республика марий эл": {"id": 1620, "cities": {"виловатово": 4228, "волжск": 1621}}},
        },
        "казахстан": {"id": 40, "regions": {"абай": {"id": 6251, "cities": {}}, "айет": {"id": 6782, "cities": {}}}},
        "азербайджан": {
            "id": 9,
            "regions": {"агдаш": {"id": 2970, "cities": {}}, "агджабеди": {"id": 2966, "cities": {}}},
        },
    }
    mock_get.assert_called_once_with("https://api.hh.ru/areas/")


@patch("requests.get")
def test_get_area_code_no_connection(mock_get: Any, capsys: Any) -> None:
    mock_get.side_effect = ConnectionError
    with mock_get.raises(ConnectionError):
        area_codes = utils.get_area_codes()
    console_message = capsys.readouterr()

    assert console_message.out == "Отсутствует подключение к сети\n"
    assert area_codes == {}
    mock_get.assert_called_once_with("https://api.hh.ru/areas/")


@pytest.mark.parametrize(
    "input_list, expected",
    [
        (["Россия", "Москва"], 1),
        (["Тайланд"], None),
        (["ГРУЗИЯ", "бАтУмИ"], 2814),
        (["россия", "республика МАРИЙ ЭЛ", "Красногорский"], 4232),
        (["Беларусь", "Брестская Область", "Антополь"], 11130),
        (["Молдова", ""], 62),
        (["Молдова", "Кишинёв"], 5049),
        (["Австралия"], 6),
        (["Россия", "Новосибирск", "Новосибирск"], 113),
        (["Беларусь", "Брестская область", "Брест"], 1007),
        (["Россия", "Подмосковье", "Москва"], 1),
        (["Россия", "Республика МАРИЙ ЭЛ", "Сосновка"], 1620),
    ],
)
@patch("src.utils.get_area_codes")
@patch("builtins.input")
def test_area_code_detector(
    mock_input: Any, mock_areas: Any, input_list: list, expected: int | None, area_codes: dict
) -> None:
    mock_input.side_effect = input_list
    mock_areas.return_value = area_codes
    assert utils.area_code_detector() == expected
    assert mock_input.call_count == len(input_list)
    mock_areas.assert_called_once_with()


@patch("requests.get")
@patch("builtins.input")
def test_area_code_detector_no_connection(mock_input: Any, mock_get: Any, capsys: Any) -> None:
    mock_input.return_value = "Россия"
    mock_get.side_effect = ConnectionError

    assert utils.area_code_detector() is None
    console_message = capsys.readouterr()
    assert (
        console_message.out == 'Отсутствует подключение к сети\nВ источнике нет информации о вакансиях в "Россия".\n'
    )
    mock_get.assert_called_once_with("https://api.hh.ru/areas/")
    mock_input.assert_called_once_with("Введите название страны: ")


@pytest.mark.parametrize("currency_code, expected", [("rub", "RUB"), ("USD", "USD"), ("EURO", "RUB")])
def test_currency_code_detector(currency_code: str, expected: str) -> None:
    assert utils.currency_code_detector(currency_code) == expected
