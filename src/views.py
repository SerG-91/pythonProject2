import datetime
import pandas as pd


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


# path= "../data/operations.csv"
def cards(path: str) -> list:
    """Функция группирует данные датафрейма по номерам карт и считает сумму трат по каждой карте"""

    df_load = pd.read_csv(path)
    df_load['Сумма операции с округлением'] = df_load['Сумма операции с округлением'].str.replace(",", ".")
    df_load['Сумма операции с округлением'] = df_load['Сумма операции с округлением'].astype('float')
    df_group_by_card = df_load.groupby('Номер карты')
    df_agg_summ = df_group_by_card['Сумма операции с округлением'].sum().to_dict()

    list_cards = []
    for i, y in df_agg_summ.items():
        list_cards.append({
            "last_digits": i[1:],
            "total_spent": y,
            "cashback": round(y/100, 2)
        })
    return list_cards


if __name__ == "__main__":
    path = "../data/operations.csv"
    output_dict = {
        "greeting": greeting(),
        "cards": cards(path)
    }

    print(output_dict)
