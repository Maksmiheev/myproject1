

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_by_currency():
    transactions = [
        {"operationAmount": {"amount": 100, "currency": {"code": "USD"}}},
        {"operationAmount": {"amount": 200, "currency": {"code": "EUR"}}},
    ]

    filtered_transactions = list(filter_by_currency(transactions, "USD"))
    expected_result = [{"operationAmount": {"amount": 100, "currency": {"code": "USD"}}}]

    assert filtered_transactions == expected_result


def test_card_number_generator_valid(valid_range):
    start, end = valid_range
    result = list(card_number_generator(start, end))
    expected_result = ["1000 0000 0000 0000", "1000 0000 0000 0001", "1000 0000 0000 0002"]
    assert result == expected_result


def test_transaction_descriptions(sample_transactions):
    expected_results = [
        "Транзакция Пополнение счета: сумма 100 RUB",
        "Транзакция неизвестно: сумма 200 USD",
        "Транзакция неизвестно: сумма  ",
    ]

    actual_results = list(transaction_descriptions(sample_transactions))

    assert actual_results == expected_results
