import pytest

from src.generators import (card_number_generator, filter_by_currency,
                            transaction_descriptions)


def test_filter_by_currency(sample_transactions, usd_transactions):
    result = filter_by_currency(sample_transactions, "USD")
    assert result == usd_transactions


def test_card_number_generator_valid(valid_range):
    start, end = valid_range
    result = list(card_number_generator(start, end))
    expected_result = ["1000 0000 0000 0000", "1000 0000 0000 0001", "1000 0000 0000 0002"]
    assert result == expected_result


def test_transaction_descriptions(sample_transactions_with_amounts, expected_descriptions):
    gen = transaction_descriptions(sample_transactions_with_amounts)
    result = list(gen)
    print(result)  # Выводим результат для диагностики
    assert result == expected_descriptions
