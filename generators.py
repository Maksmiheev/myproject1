def filter_by_currency(transactions, currency):
    """
    Возвращает итератор, выдающий транзакции с указанной валютой.
    """
    return (transaction for transaction in transactions if transaction.get('currency') == currency)


def transaction_descriptions(transactions):
    """
    Генератор, принимающий список словарей с транзакциями и выводящий описание каждой операции.
    """
    for txn in transactions:
        yield f"Транзакция {txn['description']}: сумма {txn['amount']} {txn['currency']}"

        def card_number_generator(start=1, end=9999_9999_9999_9999):
            """Генерирует последовательность банковских карточных номеров начиная с start и заканчивая end."""
            if not isinstance(start, int) or not isinstance(end, int):
                raise ValueError("Начальное и конечное значение должны быть целыми числами.")
            if start > end:
                raise ValueError("Начальное значение должно быть меньше либо равно конечному значению.")
            for num in range(start, end + 1):
                formatted_num = "{:016}".format(num)
                formatted_num = " ".join([formatted_num[i:i + 4] for i in range(0, len(formatted_num), 4)])
                yield formatted_num