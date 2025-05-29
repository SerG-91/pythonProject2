import os

import pandas as pd

from config import DATA_DIR
from src.utils import get_data_df


def search_tel(df: pd.DataFrame) -> list:
    pattern = r'\b \W+7\W\d{3}\W\d{3}-\d{2}-\d{2}'
    filtered_data = df[df['Описание'].str.contains(pattern, na=False)]
    len_list = len(filtered_data)
    output_json_list = (filtered_data.to_json(orient='records', force_ascii=False, indent=4) + "\n" +
              f"Количество записей с номерами телефонов: {len_list} шт")
    # filtered_data.to_json(os.path.join(DATA_DIR, "phone.json"), orient='records', force_ascii=False, indent=4)
    # return filtered_data.to_json(orient='records', force_ascii=False, indent=4)
    return output_json_list


def search_name(df: pd.DataFrame) -> list:
    pattern = r'\D* \D[.]$'
    filtered_data = df[df['Описание'].str.contains(pattern, na=False)]
    return filtered_data.to_json(orient='records', force_ascii=False, indent=4)


# if __name__ == "__main__":
#     path_csv = os.path.join(DATA_DIR, "operations.csv")
#     df_load = get_data_df(path_csv)
#
#     print(search_name(df_load))
