from src.views import list_top_five_transactions, cards, greeting, service_transfers_and_cash


def test_list_top_five_transactions(df, date_time):
    assert list_top_five_transactions(df, date_time) == [
        {'date': '08.06.2021', 'amount': 30.0, 'category': 'Связь', 'description': 'Devajs Servis.'},
        {'date': '09.06.2021', 'amount': 30.0, 'category': 'Частные услуги', 'description': 'IP Zizov Km'},
        {'date': '11.06.2021', 'amount': 23.73, 'category': 'Одежда и обувь', 'description': 'Детки'},
        {'date': '17.06.2021', 'amount': 20.0, 'category': 'Фастфуд', 'description': 'IP Yakubovskaya M.V.'},
        {'date': '14.06.2021', 'amount': 17.0, 'category': 'Различные товары', 'description': 'Детский Мир'}]


def test_cards(df2):
    assert cards(df2) == [{'last_digits': '5091', 'total_spent': 60.730000000000004, 'cashback': 0.61},
                          {'last_digits': '7197', 'total_spent': 60.0, 'cashback': 0.6}]


def test_greeting(time):
    assert greeting(time) == "Доброй ночи"


def test_service_transfers_and_cash(df6, date_time):
    assert service_transfers_and_cash(df6, date_time) == [{'category': 'Переводы', 'amount': 90000}, {'category': 'Наличные', 'amount': 30}]