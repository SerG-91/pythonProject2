from src.views import list_top_five_transactions, cards, greeting, service_transfers_and_cash, \
    service_amount_by_category


def test_greeting(time):
    assert greeting(time) == "Доброй ночи"


def test_cards(df6):
    assert cards(df6) == [{'last_digits': '5091', 'total_spent': 260.73, 'cashback': 2.61},
                          {'last_digits': '7197', 'total_spent': 90060.5, 'cashback': 900.61}]


def test_list_top_five_transactions(df6, date_time):
    assert list_top_five_transactions(df6, date_time) == [
        {'date': '11.06.2021', 'amount': 30.5, 'category': 'Связь', 'description': 'Переводы'},
        {'date': '09.06.2021', 'amount': 30.0, 'category': 'Наличные', 'description': 'Снятие денег'},
        {'date': '10.06.2021', 'amount': 23.73, 'category': 'Одежда и обувь', 'description': 'Детки'},
        {'date': '17.06.2021', 'amount': 20.0, 'category': 'Фастфуд', 'description': 'IP Yakubovskaya M.V.'},
        {'date': '14.06.2021', 'amount': 17.0, 'category': 'Различные товары', 'description': 'Детский Мир'}]


def test_service_amount_by_category(df6, date_time):
    assert service_amount_by_category(df6, date_time) == [{'category': 'Переводы', 'amount': 90000.0},
                                          {'category': 'Связь', 'amount': 30.5},
                                          {'category': 'Наличные', 'amount': 30.0},
                                          {'category': 'Одежда и обувь', 'amount': 23.73},
                                          {'category': 'Фастфуд', 'amount': 20.0},
                                          {'category': 'Различные товары', 'amount': 17.0},
                                          {'category': 'Остальное', 'amount': 0}]


def test_service_transfers_and_cash(df6, date_time):
    assert service_transfers_and_cash(df6, date_time) == [{'category': 'Переводы', 'amount': 90000},
                                                          {'category': 'Наличные', 'amount': 30}]
