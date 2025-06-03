import datetime
import logging
from typing import Any

import pandas as pd

from config import LOGS_DIR

logger = logging.getLogger(__name__)
logger.setLevel("INFO")
file_handler = logging.FileHandler(f"{LOGS_DIR}/views.log", encoding='utf-8')
file_formatter = logging.Formatter("%(asctime)s - %(name)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def greeting(time_now: datetime) -> str:
    """Функция реализующая приветствие от текущего времени"""

    if 0 <= time_now.hour < 6:
        logger.info("Возвращаем приветствие согласно переданной дате")
        return "Доброе утор"
    elif 6 <= time_now.hour < 12:
        logger.info("Возвращаем приветствие согласно переданной дате")
        return "Доброй днь"
    elif 12 <= time_now.hour < 18:
        logger.info("Возвращаем приветствие согласно переданной дате")
        return "Доброй вечер"
    else:
        logger.info("Возвращаем приветствие согласно переданной дате")
        return "Доброй ночи"


def cards(df: pd.DataFrame) -> list:
    """Функция группирует данные датафрейма по номерам карт и считает сумму трат по каждой карте"""

    logger.info("Группируем по необходимым признакам датафрейм для функции cards")
    df_group_by_card = df.groupby("Номер карты")
    df_agg_summ = df_group_by_card["Сумма операции с округлением"].sum().to_dict()

    list_cards = []
    for i, y in df_agg_summ.items():
        list_cards.append({"last_digits": i[1:], "total_spent": y, "cashback": round(y / 100, 2)})
    logger.info("Функция cards возвращает отредактированный список")
    return list_cards


def list_top_five_transactions(df: pd.DataFrame, data: str) -> list:
    """Функция принимает на вход датафрейм и дату, а возвращаем список 5 наибольших по сумме транзакций
    за период от введеной даты по начало этого месяца"""

    logger.info("Группируем по необходимым признакам датафрейм для функции list_top_five_transactions")
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True)
    end_data = datetime.datetime.strptime(data, "%d.%m.%Y")
    start_data = end_data.replace(day=1)
    range_time_list = df[(df["Дата платежа"] >= start_data) & (df["Дата платежа"] <= end_data)]
    top_five_transactions_sorted = range_time_list.sort_values("Сумма операции с округлением", ascending=False).tail(5)
    top_five_transactions_list = top_five_transactions_sorted.loc[
        :, ["Дата платежа", "Сумма операции с округлением", "Категория", "Описание"]
    ].to_dict("records")
    list_top_transactions = []
    for x in top_five_transactions_list:
        list_top_transactions.append(
            {
                "date": x["Дата платежа"].strftime("%d.%m.%Y"),
                "amount": x["Сумма операции с округлением"],
                "category": x["Категория"],
                "description": x["Описание"],
            }
        )
    logger.info("Функция list_top_five_transactions возвращает отредактированный список")
    return list_top_transactions


def service_total_amount(df: pd.DataFrame, data: str, range_month=0) -> Any:
    """Функция принимает на вход датафрейм, дату и период в месяцах за который будет происходить посчет,
    а возвращает общюю сумму трат за данный период времени"""

    logger.info("Группируем по необходимым признакам датафрейм для функции service_total_amount")
    end_data = datetime.datetime.strptime(data, "%d.%m.%Y")
    start_data = end_data.replace(month=end_data.month - range_month, day=1)
    range_time_list = df[(df["Дата платежа"] > start_data) & (df["Дата платежа"] <= end_data)]
    all_sum = range_time_list.agg({"Сумма операции с округлением": "sum"})
    logger.info("Функция list_top_five_transactions возвращает ускомое значение")
    return round(all_sum.to_dict()["Сумма операции с округлением"], 2)


def service_amount_by_category(df: pd.DataFrame, data: str, range_month=0) -> Any:
    """Функция принимает на вход датафрейм, дату и период в месяцах за который будет происходить посчет,
    а возвращает общюю сумму трат отсортированную от большего к меньшему за данный период времени
    по первым 7 категориям, а все остальные уходят в категорию - Остальное"""

    logger.info("Группируем по необходимым признакам датафрейм для функции service_amount_by_category")
    end_data = datetime.datetime.strptime(data, "%d.%m.%Y")
    start_data = end_data.replace(month=end_data.month - range_month, day=1)
    range_time_list = df[(df["Дата платежа"] > start_data) & (df["Дата платежа"] <= end_data)]
    category_agg_list = (
        range_time_list.groupby("Категория")
        .agg({"Сумма операции с округлением": "sum"})
        .sort_values("Сумма операции с округлением", ascending=False)
        .to_dict()
    )
    list_category = []
    char = 1
    sum_count = 0
    for i in category_agg_list.values():
        for x, t in i.items():
            if char > 7:
                sum_count += t
            else:
                list_category.append({"category": x, "amount": round(t, 2)})
            char += 1
    list_category.append({"category": "Остальное", "amount": round(sum_count, 2)})
    logger.info("Функция list_top_five_transactions возвращает отредактированный список")
    return list_category


def service_transfers_and_cash(df: pd.DataFrame, data: str, range_month=0) -> Any:
    """Функция принимает на вход датафрейм, дату и период в месяцах за который будет происходить посчет,
    а возвращает общую сумму трат по категории Наличные и Переводы"""

    logger.info("Группируем по необходимым признакам датафрейм для функции service_transfers_and_cash")
    end_data = datetime.datetime.strptime(data, "%d.%m.%Y")
    start_data = end_data.replace(month=end_data.month - range_month, day=1)
    range_time_list = df[(df["Дата платежа"] > start_data) & (df["Дата платежа"] <= end_data)]
    category_agg_list = range_time_list.groupby("Категория").agg({"Сумма операции с округлением": "sum"})
    # print(start_data, end_data)
    try:
        perevod = category_agg_list.loc["Переводы"].to_dict()
        nal = category_agg_list.loc["Наличные"].to_dict()
        list_perevod_and_nal = []
        if perevod["Сумма операции с округлением"] > nal["Сумма операции с округлением"]:
            list_perevod_and_nal.append(
                {"category": "Переводы", "amount": round(perevod["Сумма операции с округлением"])}
            )
            list_perevod_and_nal.append({"category": "Наличные", "amount": round(nal["Сумма операции с округлением"])})
        else:
            list_perevod_and_nal.append(
                {"category": "Наличные", "amount": round(perevod["Сумма операции с округлением"])}
            )
            list_perevod_and_nal.append({"category": "Переводы", "amount": round(nal["Сумма операции с округлением"])})
        logger.info("Функция service_transfers_and_cash возвращает отредактированный список")
        return list_perevod_and_nal
    except Exception as f:
        logger.warning(f"ошибка - {f}")
