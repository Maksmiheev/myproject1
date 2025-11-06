import unittest

import pytest


# Фикстуры
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
    return [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "CANCELED"}, {"id": 3, "state": "PENDING"}]


# Функция маскирования номера карты
def get_mask_card_number(card_number: str) -> str:
    """Возвращает замаскированный номер банковской карты."""
    first_part = card_number[:6]
    last_part = card_number[-4:]
    middle = "**"
    result = f"{first_part[:-2]} {middle} **** {last_part}"
    return result


# Тестирование функции маскировки карт
class TestGetMaskCardNumber(unittest.TestCase):
    """
    Класс для тестирования функции get_mask_card_number.
    Проверяются различные варианты ввода: стандартные, некорректные,
    экстремальные значения и недопустимый формат.
    """

    # Стандартный случай - правильная маска карты
    def test_standard_card_number(self):
        expected_result = "1234 ** **** 5678"
        actual_result = get_mask_card_number("123456******5678")
        self.assertEqual(actual_result, expected_result)

    # Карта, начинающаяся и заканчивающаяся одинаковыми цифрами
    def test_same_first_last_four_digits(self):
        expected_result = "1111 ** **** 1111"
        actual_result = get_mask_card_number("111111******1111")
        self.assertEqual(actual_result, expected_result)

    # Границы начала и конца маски (все нули)
    def test_zeroes_only(self):
        expected_result = "0000 ** **** 0000"
        actual_result = get_mask_card_number("0000000000000000")
        self.assertEqual(actual_result, expected_result)

    # Случай, когда номер начинается и заканчивается одним числом
    def test_single_digit_start_end(self):
        expected_result = "1111 ** **** 1111"
        actual_result = get_mask_card_number("111111******1111")
        self.assertEqual(actual_result, expected_result)

    # Входной аргумент - None
    def test_none_input(self):
        with self.assertRaises(TypeError):
            get_mask_card_number(None)


# Функция маскирования банковского счета
def get_mask_account(account_number: str) -> str:
    """Возвращает замаскированный банковский счёт в формате **XXXX."""
    if len(account_number) < 4 or not account_number.isdigit():
        raise ValueError("Номер счёта должен содержать минимум 4 цифры.")
    return f"**{account_number[-4:]}"


# Тестирование функции маскировки счетов
class TestGetMaskAccount(unittest.TestCase):

    def test_minimum_length(self):
        """Тест минимального количества цифр в счете"""
        masked_account = get_mask_account("1234")
        self.assertEqual(masked_account, "**1234")

    def test_too_short_account(self):
        """Ошибка при недостаточной длине счёта"""
        with self.assertRaises(ValueError):
            get_mask_account("123")

    def test_non_digit_account(self):
        """Ошибка при наличии небуквенных символов в номере счёта"""
        with self.assertRaises(ValueError):
            get_mask_account("ABC123")

    def test_empty_string(self):
        """Ошибка при передаче пустой строки"""
        with self.assertRaises(ValueError):
            get_mask_account("")

    def test_all_zeros(self):
        """Обработка случая, когда номер счёта состоит из одних нулей"""
        masked_account = get_mask_account("00000000")
        self.assertEqual(masked_account, "**0000")

    def test_maximum_digits(self):
        """Работа с максимально возможным числом цифр в номере счёта"""
        long_account = "1" * 100  # Генерируем большую строку из единиц
        masked_account = get_mask_account(long_account)
        self.assertEqual(masked_account, f"**{'1' * 4}")


if __name__ == "__main__":
    unittest.main()

