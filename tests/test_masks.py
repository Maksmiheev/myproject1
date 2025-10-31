import unittest

def get_mask_card_number(card_number: str) -> str:
    """Возвращает замаскированный номер банковской карты."""
    first_part = card_number[:6]
    last_part = card_number[-4:]
    middle = "**"
    result = f"{first_part[:-2]} {middle} **** {last_part}"
    return result

class TestGetMaskCardNumber(unittest.TestCase):
    """
    Класс для тестирования функции get_mask_card_number.
    Проверяются различные варианты ввода: стандартные, некорректные,
    экстремальные значения и недопустимый формат.
    """

    # Стандартный случай - правильная маска карты
    def test_standard_card_number(self):
        expected_result = '1234 ** **** 5678'
        actual_result = get_mask_card_number('123456******5678')
        self.assertEqual(actual_result, expected_result)

    # Карта, начинающаяся и заканчивающаяся одинаковыми цифрами
    def test_same_first_last_four_digits(self):
        expected_result = '1111 ** **** 1111'
        actual_result = get_mask_card_number('111111******1111')
        self.assertEqual(actual_result, expected_result)



    # Границы начала и конца маски (все нули)
    def test_zeroes_only(self):
        expected_result = '0000 ** **** 0000'
        actual_result = get_mask_card_number('0000000000000000')
        self.assertEqual(actual_result, expected_result)

    # Случай, когда номер начинается и заканчивается одним числом
    def test_single_digit_start_end(self):
        expected_result = '1111 ** **** 1111'
        actual_result = get_mask_card_number('111111******1111')
        self.assertEqual(actual_result, expected_result)

    # Входной аргумент - None
    def test_none_input(self):
        with self.assertRaises(TypeError):
            get_mask_card_number(None)

if __name__ == "__main__":
    unittest.main()