import datetime
import json
import os
from typing import Optional

import pandas as pd

from config import DATA_DIR
from src.utils import get_data_df


def save_to_file(filename=None):
    """Декоратор для записи в файл"""
    def wrapper(func):
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            if filename is None:
                file_name = f"report_{func.__name__}_{datetime.datetime.now().strftime('%d.%m.%Y')}.json"
                file_path = os.path.join(DATA_DIR, file_name)
                with open(file_path, "w", encoding='utf-8') as file:
                    json.dump(result, file, ensure_ascii=False, indent=4)
                return result
            file_name = filename
            file_path = os.path.join(DATA_DIR, file_name)
            with open(file_path, "w", encoding='utf-8') as file:
                json.dump(result, file, orient='records')
            return result
        return inner
    return wrapper


@save_to_file()
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """ Функция, которая принимает на вход: датафрейм с транзакциями, название категории и
    дату. Если дата не передана, то берется текущая дата. Функция возвращает
    траты по заданной категории за последние три месяца (от переданной даты)."""

    if date is None:
        date = datetime.datetime.now().date()
    else:
        date = datetime.datetime.strptime(date, "%d.%m.%Y")
    try:
        end_data = date
        start_data = (date - datetime.timedelta(days=90))
        range_time_list = transactions[(transactions["Дата платежа"] > start_data)
                                       & (transactions["Дата платежа"] <= end_data)]
        filter_by_category = range_time_list[range_time_list['Категория'] == category]
        return filter_by_category.to_json(orient='records', force_ascii=False, indent=4)
    except Exception as e:
        print(f"Таких данных в таблице нет - ошибка: {e}")


if __name__ == "__main__":
    path_csv = os.path.join(DATA_DIR, "operations.csv")
    df_load = get_data_df(path_csv)

    print(spending_by_category(df_load, "Фастфуд", "20.06.2021"))
