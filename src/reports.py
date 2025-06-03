import datetime
import json
import logging
import os
from typing import Optional

import pandas as pd

from config import DATA_DIR, LOGS_DIR

logger = logging.getLogger(__name__)
logger.setLevel("INFO")
file_handler = logging.FileHandler(f"{LOGS_DIR}/reports.log", encoding='utf-8')
file_formatter = logging.Formatter("%(asctime)s - %(name)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def save_to_file(filename=None):
    """Декоратор для записи в файл"""

    def wrapper(func):
        def inner(*args, **kwargs):
            logger.info("Начало работы декоратора")
            result = func(*args, **kwargs)
            if filename is None:
                file_name = f"report_{func.__name__}_{datetime.datetime.now().strftime('%d.%m.%Y')}.json"
                file_path = os.path.join(DATA_DIR, file_name)
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(result, file, ensure_ascii=False, indent=4)
                return result
            file_name = filename
            file_path = os.path.join(DATA_DIR, file_name)
            logger.info(f"Декоратор записывает данные в файл {file_path}")
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(result, file, orient="records")
            return result

        return inner

    return wrapper


@save_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция, которая принимает на вход: датафрейм с транзакциями, название категории и
    дату. Если дата не передана, то берется текущая дата. Функция возвращает
    траты по заданной категории за последние три месяца (от переданной даты)."""

    logger.info("Группируем по необходимым признакам датафрейм для функции spending_by_category")
    if date is None:
        date = datetime.datetime.now().date()
    else:
        date = datetime.datetime.strptime(date, "%d.%m.%Y")
    try:
        end_data = date
        start_data = date - datetime.timedelta(days=90)
        range_time_list = transactions[
            (transactions["Дата платежа"] > start_data) & (transactions["Дата платежа"] <= end_data)
        ]
        filter_by_category = range_time_list[range_time_list["Категория"] == category]
        logger.info("Функция spending_by_category возвращает отредактированный список")
        return filter_by_category.to_json(orient="records", force_ascii=False, indent=4)
    except Exception as e:
        logger.warning(f"ошибка - {e}")
