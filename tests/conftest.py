import pytest


@pytest.fixture
def sample_operations():
    return [
        {"type": "card", "number": "1234567890123456"},
        {"type": "account", "number": "1234567890"},
        {"type": "card", "number": "9876543210987654"},
        {"type": "account", "number": "987654321"},
    ]


@pytest.fixture
def valid_dates():
    return {
        "2024-03-11": "11.03.2024",
        "2024-01-02": "02.01.2024",
        "0001-01-01": "01.01.0001",
        "9999-12-31": "31.12.9999",
    }


@pytest.fixture
def operations_list():
    return [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "CANCELED"}, {"id": 3, "state": "EXECUTED"}]


@pytest.fixture
def transactions():
    return [{"id": 1, "date": "2023-01-01"}, {"id": 2, "date": "2023-01-03"}, {"id": 3, "date": "2023-01-02"}]


@pytest.fixture
def sample_transactions():
    return [
        {"amount": 100, "currency": "USD", "description": "Покупка товаров"},
        {"amount": 200, "currency": "EUR", "description": "Оплата услуг"},
        {"amount": 300, "currency": "USD", "description": "Возврат денежных средств"},
        {"amount": 400, "currency": "RUB", "description": "Перечисление зарплаты"},
    ]


@pytest.fixture
def expected_usd_transactions():
    return [
        {"amount": 100, "currency": "USD", "description": "Покупка товаров"},
        {"amount": 300, "currency": "USD", "description": "Возврат денежных средств"},
    ]


@pytest.fixture
def expected_transaction_descriptions():
    return [
        "Транзакция Покупка товаров: сумма 100 USD",
        "Транзакция Оплата услуг: сумма 200 EUR",
        "Транзакция Возврат денежных средств: сумма 300 USD",
        "Транзакция Перечисление зарплаты: сумма 400 RUB",
    ]
