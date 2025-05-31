import os
import datetime

from config import DATA_DIR
from src.reports import spending_by_category
from src.services import search_name, search_tel
from src.utils import get_data_df, get_api_exchange_rate, get_api_stocks_snp
from src.views import greeting, cards, list_top_five_transactions, service_total_amount, service_amount_by_category, \
    service_transfers_and_cash

path_csv = os.path.join(DATA_DIR, "operations.csv")
df_load = get_data_df(path_csv)
greeting_time = datetime.datetime.now()


def main():
    print("ГЛАВНАЯ\n")
    print("Главная:")
    output_dict_main = {
        "greeting": greeting(greeting_time),
        "cards": cards(df_load),
        "top_transactions": list_top_five_transactions(df_load, '20.06.2021'),
        # "currency_rates": get_api_exchange_rate(),
        # "stock_prices": get_api_stocks_snp()
    }
    print(output_dict_main)

    print("\nСобытия")
    output_dict_service = {
        "expenses": {"total_amount": service_total_amount(df_load, '10.07.2021', 3)},
        "main": service_amount_by_category(df_load, '10.07.2021', 3),
        "transfers_and_cash": service_transfers_and_cash(df_load, '10.07.2021', 3),
        # "currency_rates": get_api_exchange_rate(),
        # "stock_prices": get_api_stocks_snp()

    }
    print(output_dict_service)
    print("\nСЕРВИСЫ\n")
    print("Поиск по телефонным номерам:")
    print(search_tel(df_load))

    print("\nПоиск переводов физическим лицам:")
    print(search_name(df_load))


    print("\nОТЧЕТЫ\n")
    print("Траты по категории:")
    print(spending_by_category(df_load, "Фастфуд", "20.06.2021"))
    return ""

if __name__ == "__main__":
    print(main())
