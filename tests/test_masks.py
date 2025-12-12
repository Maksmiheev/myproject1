import unittest

from src.masks import get_mask_account, get_mask_card_number


class TestMaskFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_mask_card_number_valid_input(self):
        """Проверяем маску карты при правильном вводе"""
        input_data = "1234567890123456"
        expected_output = "1234 ** **** 3456"
        self.assertEqual(get_mask_card_number(input_data), expected_output)

    def test_get_mask_card_number_invalid_length(self):
        """Проверяем обработку некорректной длины картонного номера"""
        with self.assertRaises(ValueError):
            get_mask_card_number("12345678901234")

    def test_get_mask_account_valid_input(self):
        """Проверяем успешную маску банковского счета"""
        input_data = "123456789012"
        expected_output = "**9012"
        self.assertEqual(get_mask_account(input_data), expected_output)

    def test_get_mask_account_invalid_length(self):
        """Проверяем ошибку при недостаточной длине номера счета"""
        with self.assertRaises(ValueError):
            get_mask_account("123")


if __name__ == "__main__":
    unittest.main()
