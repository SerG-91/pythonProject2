import datetime

import pandas as pd
import pytest


@pytest.fixture
def df6():
    return pd.DataFrame(
        {
            "Номер карты": ["*7197", "*7197", "*5091", "*5091", "*5091", "*7197", "*5091"],
            "Дата платежа": [
                datetime.datetime(2021, 6, 11),
                datetime.datetime(2021, 6, 9),
                datetime.datetime(2021, 6, 10),
                datetime.datetime(2021, 6, 17),
                datetime.datetime(2021, 6, 14),
                datetime.datetime(2021, 6, 20),
                datetime.datetime(2021, 7, 13),
            ],
            "Сумма операции с округлением": [30.5, 30.0, 23.73, 20.0, 17.0, 90000.00, 200.00],
            "Категория": [
                "Связь",
                "Наличные",
                "Одежда и обувь",
                "Фастфуд",
                "Различные товары",
                "Переводы",
                "Мобильная связь",
            ],
            "Описание": [
                "Переводы",
                "Снятие денег",
                "Детки",
                "IP Yakubovskaya M.V.",
                "Детский Мир",
                "Иван С.",
                "Тинькофф Мобайл +7 995 555-55-55",
            ],
        }
    )


@pytest.fixture
def date_time():
    return "20.06.2021"


@pytest.fixture
def time():
    return datetime.datetime(year=2025, month=5, day=1, hour=18, minute=30, second=00)


@pytest.fixture
def category():
    return "Фастфуд"
