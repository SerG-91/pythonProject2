import os

import pandas as pd

from config import DATA_DIR
from src.utils import get_data_df


def search_tel(df: pd.DataFrame) -> None:
    pattern = r'\b \W+7\W\d{3}\W\d{3}-\d{2}-\d{2}'
    filtered_data = df[df['Описание'].str.contains(pattern, na=False)]
    # filtered_data.to_json(os.path.join(DATA_DIR, "phone.json"), orient='records', force_ascii=False, indent=4)
    return filtered_data.to_json(orient='records', force_ascii=False, indent=4)


if __name__ == "__main__":
    path_csv = os.path.join(DATA_DIR, "operations.csv")
    df_load = get_data_df(path_csv)

    t = pd.DataFrame({
        "Номер карты": ["*7197", "*7197", "*5091", "*5091", "*5091", "*5091"],
        "Дата платежа": ["08.06.2021", "09.06.2021", "11.06.2021", "17.06.2021", "14.06.2021", "19.11.2021"],
        "Сумма операции с округлением": ["30,0", "30,0", "23,73", "20,0", "17,0", "200,00"],
        "Категория": ["Связь", "Частные услуги", "Одежда и обувь", "Фастфуд", "Различные товары", "Мобильная связь"],
        "Описание": ["Devajs Servis.", "IP Zizov Km", "Детки", "IP Yakubovskaya M.V.", "Детский Мир", "Тинькофф "
                                                                                                      "Мобайл +7 995 "
                                                                                                      "555-55-55"]
    })
    print(search_tel(t))
