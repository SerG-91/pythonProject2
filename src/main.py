import os
import datetime

from config import DATA_DIR
from src.services import search_name, search_tel
from src.utils import get_data_df
from src.views import greeting, cards, list_top_five_transactions

path_csv = os.path.join(DATA_DIR, "operations.csv")
df_load = get_data_df(path_csv)
greeting_time = datetime.datetime.now()

print("ГЛАВНАЯ")
output_dict = {
        "greeting": greeting(greeting_time),
        "cards": cards(df_load),
        "top_transactions": list_top_five_transactions(df_load, '20.06.2021')
    }
print(output_dict)

print("СЕРВИСЫ")
print(search_name(df_load))
print(search_tel(df_load))
