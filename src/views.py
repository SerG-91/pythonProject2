import datetime
import os.path

import pandas as pd

from config import DATA_DIR
from src.utils import get_data_df


def greeting() -> str:
    """ Функция реализующая приветствие от текущего времени"""

    greeting_time = datetime.datetime.now()
    if 0 <= greeting_time.hour <= 6:
        return 'Доброй ночи'
    elif 6 < greeting_time.hour <= 12:
        return 'Доброй утро'
    elif 12 < greeting_time.hour <= 18:
        return 'Доброй день'
    else:
        return 'Доброй вечер'


def cards(df: pd.DataFrame) -> list:
    """Функция группирует данные датафрейма по номерам карт и считает сумму трат по каждой карте"""

    df_load['Сумма операции с округлением'] = df_load['Сумма операции с округлением'].str.replace(",", ".")
    df_load['Сумма операции с округлением'] = df_load['Сумма операции с округлением'].astype('float')
    df_group_by_card = df_load.groupby('Номер карты')
    df_agg_summ = df_group_by_card['Сумма операции с округлением'].sum().to_dict()

    list_cards = []
    for i, y in df_agg_summ.items():
        list_cards.append({
            "last_digits": i[1:],
            "total_spent": y,
            "cashback": round(y / 100, 2)
        })
    return list_cards


def list_top_five_transactions(df: pd.DataFrame) -> list:
    df_load["Дата платежа"] = pd.to_datetime(df_load["Дата платежа"], dayfirst=True)
    input_data = input("Введите дату: ")
    end_data = datetime.datetime.strptime(input_data, "%d.%m.%Y")
    start_data = end_data.replace(day=1)
    f = df_load[(df_load["Дата платежа"] >= start_data) & (df_load["Дата платежа"] <= end_data)]
    f1 = f.sort_values("Сумма операции с округлением", ascending=False).tail(5)
    f2 = f1.loc[:, ["Дата платежа", "Сумма операции с округлением", "Категория", "Описание"]].to_dict('records')
    list_top_transactions = []
    for x in f2:
        list_top_transactions.append({
            "date": x["Дата платежа"].strftime("%d.%m.%Y"),
            "amount": x["Сумма операции с округлением"],
            "category": x["Категория"],
            "description": x["Описание"]
        })
    return list_top_transactions


if __name__ == "__main__":
    path_csv = os.path.join(DATA_DIR, "operations.csv")
    df_load = get_data_df(path_csv)

    output_dict = {
        "greeting": greeting(),
        "cards": cards(df_load),
        "top_transactions": list_top_five_transactions(df_load)
    }

    print(output_dict)
    # print(list_top_five_transactions(path))
