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
    """ Фикстура для набора транзакций """
    return [
        {
            "operationAmount": {"amount": 100, "currency": {"code": "RUB"}},
            "description": "Пополнение счета"
        },
        {
            "operationAmount": {"amount": 200, "currency": {"code": "USD"}}
        },
        {}
    ]


@pytest.fixture
def usd_transactions():
    return [
        {"currency": "USD", "amount": 100},
        {"currency": "USD", "amount": 300},
    ]


def expected_usd_transactions():
    return [
        {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}},
        {"operationAmount": {"amount": "300", "currency": {"code": "USD"}}},
    ]


@pytest.fixture
def expected_transaction_descriptions():
    return [
        "Транзакция Покупка товаров: сумма 100 USD",
        "Транзакция Оплата услуг: сумма 200 EUR",
        "Транзакция Возврат денежных средств: сумма 300 USD",
        "Транзакция Перечисление зарплаты: сумма 400 RUB",
    ]


@pytest.fixture
def valid_range():
    return (1000_0000_0000_0000, 1000_0000_0000_0002)


@pytest.fixture
def invalid_start_value():
    return ("abc", 1000_0000_0000_0002)


@pytest.fixture
def invalid_end_value():
    return (1000_0000_0000_0002, "xyz")


@pytest.fixture
def reverse_range():
    return (1000_0000_0000_0002, 1000_0000_0000_0000)


@pytest.fixture
def sample_transactions_with_amounts():
    return [
        {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}, "description": "Покупка"},
        {"operationAmount": {"amount": "200", "currency": {"code": "EUR"}}, "description": "Операция"},
        {
            "operationAmount": {"amount": None, "currency": {"code": None}},
            "description": "Без суммы",
        },  # Случай полного отсутствия данных
    ]


@pytest.fixture
def expected_descriptions():
    return [
        "Транзакция Покупка: сумма 100 USD",
        "Транзакция Операция: сумма 200 EUR",
        "Транзакция Без суммы: сумма (сумма неизвестна) (валюта неизвестна)",
    ]
