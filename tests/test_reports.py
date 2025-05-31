from src.reports import spending_by_category


def test_spending_by_category(df6, category, date_time):
    assert spending_by_category(df6, category, date_time) == ('[\n    {\n        "Номер карты":"*5091",\n        "Дата '
                                                              'платежа":1623888000000,\n        "Сумма операции с '
                                                              'округлением":20.0,\n        "Категория":"Фастфуд",'
                                                              '\n        "Описание":"IP Yakubovskaya M.V."\n    }\n]')
