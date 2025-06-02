import datetime
import logging
import os

import pandas as pd
import requests
from dotenv import load_dotenv

from config import DATA_DIR


logger = logging.getLogger("utils")
logger.setLevel("INFO")
file_handler = logging.FileHandler("logs/utils.log")
file_formatter = logging.Formatter("%(asctime)s - %(name)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

load_dotenv()

api_key = os.getenv("API_KEY")
api_stocks = os.getenv("api_stocks")


def get_data_df(path: str) -> pd.DataFrame:
    """Функция получения датафрейма из файла operations.csv"""

    logger.info("Считываем данные по указанному пути")
    df = pd.read_csv(path)
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True)
    df["Сумма операции с округлением"] = df["Сумма операции с округлением"].str.replace(",", ".")
    df["Сумма операции с округлением"] = df["Сумма операции с округлением"].astype("float")
    logger.info("Возвращаем датафрейм")
    return df


def get_api_exchange_rate() -> list:
    """Функция выводит курсы валют евро и доллара"""

    logger.info("Производим запрос курсов валют через API ключ")
    url = "https://api.apilayer.com/fixer/convert"
    payload1 = {"amount": "1", "from": "EUR", "to": "RUB"}
    payload2 = {"amount": "1", "from": "USD", "to": "RUB"}
    headers = {"apikey": api_key}
    resp_1 = requests.get(url, payload1, headers=headers).json()
    resp_2 = requests.get(url, payload2, headers=headers).json()
    resp_eur = resp_1["info"]["rate"]
    resp_usd = resp_2["info"]["rate"]

    output_list = [{"currency_rates": [{"currency": "USD", "rate": resp_usd}, {"currency": "EUR", "rate": resp_eur}]}]
    logger.info("Получаем ответ")
    return output_list


def get_api_stocks_snp(stocks) -> list:
    """Функция возвращает стоимости акций из списка S&P 500"""
    logger.info("Производим запрос акций через API ключ")
    price_stocks = []

    for stock in stocks:
        response = requests.get(f"http://api.marketstack.com/v1/eod?access_key={api_stocks}&symbols={stock}")
        dict_result = response.json()
        price_stocks.append({"stock": dict_result["data"][0]["symbol"], "price": dict_result["data"][0]["open"]})
    logger.info("Получаем ответ")
    return price_stocks


