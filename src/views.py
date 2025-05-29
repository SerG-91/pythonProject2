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
    end_data = datetime.datetime.strptime(data, "%d.%m.%Y")
    start_data = end_data.replace(day=1)
    range_time_list = df[(df["Дата платежа"] >= start_data) & (df["Дата платежа"] <= end_data)]
    top_five_transactions_sorted = range_time_list.sort_values("Сумма операции с округлением", ascending=False).tail(5)
    top_five_transactions_list = top_five_transactions_sorted.loc[:,
                                 ["Дата платежа", "Сумма операции с округлением", "Категория", "Описание"]].to_dict(
        'records')
    list_top_transactions = []
    for x in top_five_transactions_list:
        list_top_transactions.append({
            "date": x["Дата платежа"].strftime("%d.%m.%Y"),
            "amount": x["Сумма операции с округлением"],
            "category": x["Категория"],
            "description": x["Описание"]
        })
    return list_top_transactions


def service_1(df: pd.DataFrame, data: str, range_month=0) -> list:
    end_data = datetime.datetime.strptime(data, "%d.%m.%Y")
    start_data = end_data.replace(month=end_data.month - range_month, day=1)
    range_time_list = df[(df["Дата платежа"] > start_data) & (df["Дата платежа"] <= end_data)]
    all_sum = range_time_list.agg({"Сумма операции с округлением": "sum"})
    # t = range_time_list.groupby("Категория").apply(lambda x: x.sort_values("Сумма операции с округлением", ascending=False))
    # category_agg_list = range_time_list.groupby("Категория").agg({"Сумма операции с округлением": "sum"}).sort_values("Сумма операции с округлением", ascending=False).to_json(orient='records', force_ascii=False)
    return all_sum.to_dict()['Сумма операции с округлением']


def service_2(df: pd.DataFrame, data: str, range_month=0):
    end_data = datetime.datetime.strptime(data, "%d.%m.%Y")
    start_data = end_data.replace(month=end_data.month - range_month, day=1)
    range_time_list = df[(df["Дата платежа"] > start_data) & (df["Дата платежа"] <= end_data)]
    category_agg_list = range_time_list.groupby("Категория").agg({"Сумма операции с округлением": "sum"}).sort_values(
        "Сумма операции с округлением", ascending=False).to_dict()
    list_catgory = []
    char = 1
    sum_count = 0
    for i in category_agg_list.values():
        for x, t in i.items():
            if char > 7:
                sum_count += t
            else:
                list_catgory.append(
                    {
                        'category': x,
                        'amount': t
                    }
                )
            char += 1
    list_catgory.append(
        {
            'category': "Остальное",
            'amount': sum_count
        }
    )
    return list_catgory


def service_3(df: pd.DataFrame, data: str, range_month=0):
    end_data = datetime.datetime.strptime(data, "%d.%m.%Y")
    start_data = end_data.replace(month=end_data.month - range_month, day=1)
    range_time_list = df[(df["Дата платежа"] > start_data) & (df["Дата платежа"] <= end_data)]
    category_agg_list = range_time_list.groupby("Категория").agg({"Сумма операции с округлением": "sum"})
    perevod = category_agg_list.loc["Переводы"].to_dict()
    nal = category_agg_list.loc["Наличные"].to_dict()
    list_perevod_and_nal = []
    if perevod['Сумма операции с округлением'] > nal['Сумма операции с округлением']:
        list_perevod_and_nal.append({
            "category": "Переводы",
            "amount": round(perevod['Сумма операции с округлением'])
        })
        list_perevod_and_nal.append({
            "category": "Наличные",
            "amount": round(nal['Сумма операции с округлением'])
        })
    else:
        list_perevod_and_nal.append({
            "category": "Наличные",
            "amount": round(perevod['Сумма операции с округлением'])
        })
        list_perevod_and_nal.append({
            "category": "Переводы",
            "amount": round(nal['Сумма операции с округлением'])
        })
    return list_perevod_and_nal
    # print(perevod, nal)


if __name__ == "__main__":
    # greeting_time = datetime.datetime.now()
    path_csv = os.path.join(DATA_DIR, "operations.csv")
    df_load = get_data_df(path_csv)

    output_dict = {
        "expenses": {"total_amount": service_1(df_load, '10.07.2021', 3)},
        "main": service_2(df_load, '10.07.2021', 3),
        "transfers_and_cash": service_3(df_load, '10.07.2021', 3)
        # "top_transactions": list_top_five_transactions(df_load, '20.06.2021')
    }
    print(output_dict)
    # print(service_3(df_load, '10.07.2021', 3))
