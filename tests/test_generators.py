import pytest

from generators import (card_number_generator, filter_by_currency,transaction_descriptions)


def test_filter_by_currency(sample_transactions, expected_usd_transactions):
    result = list(filter_by_currency(sample_transactions, "USD"))
    assert result == expected_usd_transactions


def test_card_number_generator():
    gen = card_number_generator()
    first_few_cards = []
    for _ in range(5):
        first_few_cards.append(next(gen))

    # Проверяем форматы первых пяти значений
    assert first_few_cards == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]
    # Проверяем обработку неверных аргументов
    with pytest.raises(ValueError):
        next(card_number_generator("a", 1))  # Неверный начальный аргумент
    with pytest.raises(ValueError):
        next(card_number_generator(1, "b"))  # Неверный конечный аргумент
    with pytest.raises(ValueError):
        next(card_number_generator(10, 1))  #
