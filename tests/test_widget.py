import unittest
import pytest
from datetime import datetime


# Функции маскирования номеров
def mask_card(number: str) -> str:
    """Маскирует карту следующим образом: первые 6 и последние 4 цифры видны, остальные заменены звездочками (*)."""
    return number[:6] + "*" * (len(number) - 10) + number[-4:]


def mask_account(number: str) -> str:
    """Маскирует счет, показывая только последние 4 цифры."""
    return "*" * (len(number) - 4) + number[-4:]


def mask_account_card(input_str: str) -> str:
    """Маскирует счет или карту, исходя из указанного имени (счет или карта)."""
    parts = input_str.split()
    number = parts[-1]
    name = " ".join(parts[:-1])

    if name.lower().startswith("счет"):
        masked_number = mask_account(number)
    else:
        masked_number = mask_card(number)

    return f"{name} {masked_number}"


# Функция обработки даты
def get_date(date_str: str) -> str:
    """Преобразует дату из строки в формате ISO (YYYY-MM-DD) в формат dd.mm.yyyy."""
    dt = datetime.fromisoformat(date_str)
    return dt.strftime("%d.%m.%Y")


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
    return [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "CANCELED"}, {"id": 3, "state": "EXECUTED"}]


@pytest.fixture
def transactions():
    return [{"id": 1, "date": "2023-01-01"}, {"id": 2, "date": "2023-01-03"}, {"id": 3, "date": "2023-01-02"}]


# Юнит-тесты для функций маскирования
class TestMaskAccountCard(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_incorrect_input_type(self):
        """Тестируем обработку неправильного типа входных данных."""
        incorrect_input = "Неправильный формат 1234567890"
        try:
            mask_account_card(incorrect_input)
        except Exception as e:
            self.fail(f"Ошибка при обработке неправильного формата: {e}")

    def test_empty_string(self):
        """Тестируем реакцию на пустой ввод."""
        empty_input = ""
        with self.assertRaises(IndexError):
            mask_account_card(empty_input)


# Юнит-тесты для функции преобразование даты
class TestGetDateFunction(unittest.TestCase):
    def test_valid_iso_format(self):
        """Проверка корректного преобразования строки в формате ISO."""
        input_date = "2024-03-11"
        expected_output = "11.03.2024"
        output = get_date(input_date)
        self.assertEqual(output, expected_output)

    def test_leading_zeros(self):
        """Проверка сохранения начальных нулей в дне и месяце."""
        input_date = "2024-01-02"
        expected_output = "02.01.2024"
        output = get_date(input_date)
        self.assertEqual(output, expected_output)

    def test_invalid_format_raises_exception(self):
        """Проверка исключения при передаче некорректного формата даты."""
        invalid_date = "invalid-date-format"
        with self.assertRaises(ValueError):
            get_date(invalid_date)


if __name__ == "__main__":
    unittest.main()
