import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')


def get_data_df(path: str) -> pd.DataFrame:
    """Функция получения датафрейма из файла operations.csv"""

    df = pd.read_csv(path)
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True)
    df['Сумма операции с округлением'] = df['Сумма операции с округлением'].str.replace(",", ".")
    df['Сумма операции с округлением'] = df['Сумма операции с округлением'].astype('float')
    return df


def get_api_exchange_rate():
    """Функция выводит курсы валют евро и доллара"""

    url = "https://api.apilayer.com/fixer/convert"
    payload1 = {
        "amount": "1",
        "from": "EUR",
        "to": "RUB"
    }
    payload2 = {
        "amount": "1",
        "from": "USD",
        "to": "RUB"
    }
    headers = {
         "apikey": api_key

    }
    resp_1 = requests.get(url, payload1, headers=headers).json()
    resp_2 = requests.get(url, payload2, headers=headers).json()
    resp_eur = resp_1["info"]["rate"]
    resp_usd = resp_2["info"]["rate"]

    output_list = [{
        "currency_rates": [{
            "currency": "USD",
            "rate": resp_usd
        },
        {
            "currency": "EUR",
            "rate": resp_eur
        }
        ]
    }]

    return output_list


def get_api_stocks_snp():
    """Функция возвращает стоимости акций из списка S&P 500"""

    stocks_list = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    price_stocks = []

    for stock in stocks_list:
        response = requests.get(f"http://api.marketstack.com/v1/eod?access_key=32e2902ea866bcfcf9a8aa200fdbaac2&symbols={stock}")
        dict_result = response.json()
        price_stocks.append({
            "stock": dict_result["data"][0]["symbol"],
            "price": dict_result["data"][0]["open"]
        })
    return price_stocks
