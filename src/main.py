import datetime
import logging
import os

from config import DATA_DIR
from src.reports import spending_by_category
from src.services import search_name, search_tel
from src.utils import get_api_exchange_rate, get_api_stocks_snp, get_data_df
from src.views import (cards, greeting, list_top_five_transactions, service_amount_by_category, service_total_amount,
                       service_transfers_and_cash)

logger = logging.getLogger("main")
logger.setLevel("INFO")
file_handler = logging.FileHandler("logs/main.log")
file_formatter = logging.Formatter("%(asctime)s - %(name)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


path_csv = os.path.join(DATA_DIR, "operations.csv")
df_load = get_data_df(path_csv)
greeting_time = datetime.datetime.now()
stocks_list = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]


def main() -> None:
    logger.info("Старт работы раздела Главная")
    print("ГЛАВНАЯ\n")
    print("Главная:")
    output_dict_main = {
        "greeting": greeting(greeting_time),
        "cards": cards(df_load),
        "top_transactions": list_top_five_transactions(df_load, "20.06.2021"),
        # "currency_rates": get_api_exchange_rate(),
        # "stock_prices": get_api_stocks_snp(stocks_list)
    }
    print(output_dict_main)

    print("\nСобытия")
    output_dict_service = {
        "expenses": {"total_amount": service_total_amount(df_load, "10.07.2021", 3)},
        "main": service_amount_by_category(df_load, "10.07.2021", 3),
        "transfers_and_cash": service_transfers_and_cash(df_load, "10.07.2021", 3),
        # "currency_rates": get_api_exchange_rate(),
        # "stock_prices": get_api_stocks_snp(stocks_list)
    }
    print(output_dict_service)

    logger.info("Старт работы раздела Сервисы")
    print("\nСЕРВИСЫ\n")
    print("Поиск по телефонным номерам:")
    print(search_tel(df_load))

    print("\nПоиск переводов физическим лицам:")
    print(search_name(df_load))

    logger.info("Старт работы раздела Отчеты")
    print("\nОТЧЕТЫ\n")
    print("Траты по категории:")
    print(spending_by_category(df_load, "Фастфуд", "20.06.2021"))


if __name__ == "__main__":
    main()
