from typing import Any
from unittest.mock import patch

from requests.exceptions import ConnectionError

from src import utils


@patch("requests.get")
def test_get_area_code(mock_get: Any) -> None:
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
    area_codes = utils.get_area_code()
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
        area_codes = utils.get_area_code()
    console_message = capsys.readouterr()

    assert console_message.out == "Отсутствует подключение к сети\n"
    assert area_codes == {}
    mock_get.assert_called_once_with("https://api.hh.ru/areas/")


# @patch("requests.get")
# def test_get_response_invalid_response(mock_get: Any) -> None:
#     mock_get.return_value.status_code = 400
#     hhr_object = HHResearch()
#     vacancies = hhr_object.get_response()
#     assert vacancies == []
#     assert mock_get.call_count == 20
#     assert hhr_object._status_code == 400


# @patch("requests.get")
# def test_get_response_no_connection(mock_get: Any) -> None:
#     mock_get.side_effect = ConnectionError
#     hhr_object = HHResearch()
#     with mock_get.raises(ConnectionError):
#         hhr_object.get_response()
#
#
#     assert hhr_object._response == []
#     mock_get.assert_called_once_with(
#         "https://api.hh.ru/vacancies",
#         headers={"User-Agent": "HH-User-Agent"},
#         params=({"page": 0, "per_page": 100, "text": None, "area": None}),
#     )
