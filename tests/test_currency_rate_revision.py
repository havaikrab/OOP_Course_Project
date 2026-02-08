from typing import Any
from unittest.mock import patch

from requests.exceptions import ConnectionError

from src.currency_rate_revision import ApilayerRates


@patch("os.getenv")
def test_apilayer_rates_init(mock_env: Any) -> None:

    mock_env.return_value = "123"
    apilayer_object = ApilayerRates("EUR")

    assert apilayer_object.currency == "EUR"
    assert apilayer_object.last_update == 0
    assert apilayer_object.headers == {"apikey": "123"}
    assert apilayer_object.params == {"source": "EUR"}
    assert apilayer_object.url == "https://api.apilayer.com/currency_data/live"
    assert apilayer_object.params == {"source": "EUR"}
    assert apilayer_object._rates == {}
    mock_env.assert_called_once_with("exchangerates_API_KEY")


@patch("time.time")
@patch("requests.get")
@patch("os.getenv")
def test_get_response_update_rates(mock_env: Any, mock_get: Any, mock_time: Any) -> None:
    mock_time.return_value = 1770525000
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
        "timestamp": 1770517000,
    }
    apilayer_object = ApilayerRates("RUB")
    assert apilayer_object.last_update == 0
    assert apilayer_object._rates == {}
    mock_env.assert_called_once_with("exchangerates_API_KEY")

    apilayer_object.get_response()
    assert apilayer_object.last_update == 1770517000
    assert apilayer_object._rates == {
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


@patch("time.time")
@patch("requests.get")
def test_get_response_use_current_rates(mock_get: Any, mock_time: Any) -> None:
    mock_time.return_value = 1770525000
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = "Что-то"
    apilayer_object = ApilayerRates("EUR")
    apilayer_object.last_update = 1770523000
    apilayer_object._rates = {"Статус обновления": "Не требуется"}
    apilayer_object.get_response()

    assert apilayer_object.last_update == 1770523000
    assert apilayer_object._rates == {"Статус обновления": "Не требуется"}
    mock_time.assert_called_once_with()
    mock_get.assert_not_called()


@patch("time.time")
@patch("requests.get")
def test_get_bad_response(mock_get: Any, mock_time: Any) -> None:
    mock_time.return_value = 1770525000
    mock_get.return_value.status_code = 400
    mock_get.return_value.json.return_value = "Ничего"
    apilayer_object = ApilayerRates("EUR")
    apilayer_object.last_update = 1770520000
    apilayer_object._rates = {"Статус обновления": "Устарело"}
    apilayer_object.get_response()

    assert apilayer_object.last_update == 1770520000
    assert apilayer_object._rates == {"Статус обновления": "Устарело"}
    mock_time.assert_called_once_with()
    mock_get.assert_called_once()


@patch("requests.get")
def test_get_response_no_connection(mock_get: Any, capsys: Any) -> None:
    mock_get.side_effect = ConnectionError
    apilayer_object = ApilayerRates("USD")
    with mock_get.raises(ConnectionError):
        apilayer_object.get_response()
    console_message = capsys.readouterr()

    assert console_message.out == "Отсутствует подключение к сети, курс валюты может быть устаревшим\n"
    assert apilayer_object.last_update == 0
    assert apilayer_object._rates == {}
