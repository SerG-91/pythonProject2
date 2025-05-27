import datetime
import os.path

import pandas as pd

from config import DATA_DIR
from src.utils import get_data_df


def greeting(time_now) -> str:
    """ Функция реализующая приветствие от текущего времени"""

    if 0 <= time_now.hour < 6:
        return 'Доброе утор'
    elif 6 <= time_now.hour < 12:
        return 'Доброй днь'
    elif 12 <= time_now.hour < 18:
        return 'Доброй вечер'
    else:
        return 'Доброй ночи'


def cards(df: pd.DataFrame) -> list:
    """Функция группирует данные датафрейма по номерам карт и считает сумму трат по каждой карте"""

    df['Сумма операции с округлением'] = df['Сумма операции с округлением'].str.replace(",", ".")
    df['Сумма операции с округлением'] = df['Сумма операции с округлением'].astype('float')
    df_group_by_card = df.groupby('Номер карты')
    df_agg_summ = df_group_by_card['Сумма операции с округлением'].sum().to_dict()

    list_cards = []
    for i, y in df_agg_summ.items():
        list_cards.append({
            "last_digits": i[1:],
            "total_spent": y,
            "cashback": round(y / 100, 2)
        })
    return list_cards


def list_top_five_transactions(df: pd.DataFrame, data: str) -> list:
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True)
    # print(df)
    # input_data = input("Введите дату: ")
    end_data = datetime.datetime.strptime(data, "%d.%m.%Y")
    start_data = end_data.replace(day=1)
    f = df[(df["Дата платежа"] >= start_data) & (df["Дата платежа"] <= end_data)]
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
    greeting_time = datetime.datetime.now()
    path_csv = os.path.join(DATA_DIR, "operations.csv")
    df_load = get_data_df(path_csv)

    output_dict = {
        "greeting": greeting(greeting_time),
        "cards": cards(df_load),
        "top_transactions": list_top_five_transactions(df_load, '20.06.2021')
    }
    print(output_dict)

