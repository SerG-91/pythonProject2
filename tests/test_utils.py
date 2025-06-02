from unittest.mock import patch

from src.utils import get_api_exchange_rate, get_api_stocks_snp


@patch("requests.get")
def test_get_stock_prices(mock_get):
    stocks = ["AAPL"]
    mock_get.return_value.json.return_value = {"data": [{"open": 150, "symbol": "AAPL"}]}
    assert get_api_stocks_snp(stocks) == [{"price": 150, "stock": "AAPL"}]


@patch("requests.get")
def test_get_api_exchange_rate(mock_get):
    mock_get.return_value.json.return_value = {"info": {"rate": 10}}
    assert get_api_exchange_rate() == [
        {"currency_rates": [{"currency": "USD", "rate": 10}, {"currency": "EUR", "rate": 10}]}
    ]
