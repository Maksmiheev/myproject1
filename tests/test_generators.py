import pytest

@pytest.fixture
def sample_transactions():
    return [
        {'amount': 100, 'currency': 'USD', 'description': 'Покупка товаров'},
        {'amount': 200, 'currency': 'EUR', 'description': 'Оплата услуг'},
        {'amount': 300, 'currency': 'USD', 'description': 'Возврат денежных средств'},
        {'amount': 400, 'currency': 'RUB', 'description': 'Перечисление зарплаты'}
    ]

@pytest.fixture
def expected_usd_transactions():
    return [
        {'amount': 100, 'currency': 'USD', 'description': 'Покупка товаров'},
        {'amount': 300, 'currency': 'USD', 'description': 'Возврат денежных средств'}
    ]

@pytest.fixture
def expected_transaction_descriptions():
    return [
        "Транзакция Покупка товаров: сумма 100 USD",
        "Транзакция Оплата услуг: сумма 200 EUR",
        "Транзакция Возврат денежных средств: сумма 300 USD",
        "Транзакция Перечисление зарплаты: сумма 400 RUB"
    ]

def test_filter_by_currency(sample_transactions, expected_usd_transactions):
    result = list(filter_by_currency(sample_transactions, 'USD'))
    assert result == expected_usd_transactions

def test_transaction_descriptions(sample_transactions, expected_transaction_descriptions):
    result = list(transaction_descriptions(sample_transactions))
    assert result == expected_transaction_descriptions

def test_card_number_generator():
    generator = card_number_generator(1, 3)
    results = list(generator)
    expected_results = ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]
    assert results == expected_results