import json
import os
from typing import Any
from unittest.mock import patch

from requests.exceptions import ConnectionError

from src.currency_rate_revision import ApilayerRates


@patch("os.getenv")
def test_apilayer_rates_init(mock_env: Any) -> None:

    mock_env.return_value = "123"
    apilayer_object = ApilayerRates("EUR", filename="test_data/test_rates.json")

    assert apilayer_object.currency == "EUR"
    assert apilayer_object.filename == "test_data/test_rates.json"
    assert apilayer_object.status == "Устаревший"
    assert apilayer_object.last_update == 0
    assert apilayer_object.headers == {"apikey": "123"}
    assert apilayer_object.params == {"source": "EUR"}
    assert apilayer_object.url == "https://api.apilayer.com/currency_data/live"
    assert apilayer_object.params == {"source": "EUR"}
    assert apilayer_object.rates == {}
    mock_env.assert_called_once_with("exchangerates_API_KEY")


@patch("time.time")
@patch("requests.get")
@patch("os.getenv")
def test_get_response_reusability(mock_env: Any, mock_get: Any, mock_time: Any) -> None:
    """Тест основополагающего метода get_response. Здесь испытывается поведение метода в зависимости от срока давности
    последнего запроса курса валют"""

    os.makedirs("test_data", exist_ok=True)
    with open("test_data/test_rates.json", "w", encoding="utf-8") as file:
        json.dump(dict(), file)
    mock_time.return_value = 1770517000
    mock_env.return_value = "123"
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "quotes": {
            "RUBBYR": 255.232111,
            "RUBCNY": 0.090359,
            "RUBEUR": 0.011019,
            "RUBKGS": 1.138783,
            "RUBKZT": 6.424188,
            "RUBUAH": 0.55771,
            "RUBUSD": 0.013022,
        },
        "source": "RUB",
        "success": True,
        "timestamp": 1770516000,
    }
    apilayer_object = ApilayerRates("RUB", filename="test_data/test_rates.json")
    assert apilayer_object.last_update == 0
    assert apilayer_object.rates == {}
    mock_env.assert_called_once_with("exchangerates_API_KEY")

    apilayer_object.get_response()
    assert apilayer_object.last_update == 1770516000
    assert apilayer_object.rates == {
        "BYR": 255.232111,
        "CNY": 0.090359,
        "EUR": 0.011019,
        "KGS": 1.138783,
        "KZT": 6.424188,
        "UAH": 0.55771,
        "USD": 0.013022,
    }
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/currency_data/live", headers={"apikey": "123"}, params={"source": "RUB"}
    )
    mock_time.assert_called_once_with()
    with open("test_data/test_rates.json", "r", encoding="utf-8") as file:
        assert json.load(file) == {
            "RUB": {
                "last_update": 1770516000,
                "rates": {
                    "BYR": 255.232111,
                    "CNY": 0.090359,
                    "EUR": 0.011019,
                    "KGS": 1.138783,
                    "KZT": 6.424188,
                    "UAH": 0.55771,
                    "USD": 0.013022,
                },
            }
        }

    apilayer_object.get_response()
    assert mock_time.call_count == 4
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/currency_data/live", headers={"apikey": "123"}, params={"source": "RUB"}
    )

    os.remove("test_data/test_rates.json")
    apilayer_object.last_update = 1770510000
    apilayer_object.get_response()
    assert mock_time.call_count == 5
    assert mock_get.call_count == 2

    os.remove("test_data/test_rates.json")


@patch("requests.get")
def test_get_response_no_connection(mock_get: Any) -> None:
    mock_get.side_effect = ConnectionError
    apilayer_object = ApilayerRates("EUR", filename="test_data/test_rates.json")
    apilayer_object.get_response()

    assert apilayer_object.status == "Дисконнект"
    assert apilayer_object.rates == dict()
    assert mock_get.call_count == 1

    os.remove("test_data/test_rates.json")


@patch("time.time")
@patch("requests.get")
def test_get_bad_response(mock_get: Any, mock_time: Any) -> None:
    mock_time.return_value = 1770525000
    mock_get.return_value.status_code = 401
    apilayer_object = ApilayerRates("EUR", filename="test_data/test_rates.json")
    apilayer_object.get_response()

    assert apilayer_object.status == "Не авторизован"
    assert apilayer_object.last_update == 0
    assert mock_get.call_count == 1

    os.remove("test_data/test_rates.json")
