import unittest
from src.widget import mask_card, mask_account, mask_account_card, get_date


class TestUtilsModule(unittest.TestCase):

    def test_mask_card(self):
        """Проверка маскировки банковской карты"""
        self.assertEqual(mask_card("1234567890123456"), "123456**********3456")

    def test_mask_account(self):
        """Проверка маскировки банковского счета"""
        self.assertEqual(mask_account("40817810999910000001"), "**************0001")

    def test_mask_account_card_full(self):
        """Проверка полной маски для строки с номером карты/счета"""
        # Карта
        self.assertEqual(mask_account_card("Visa Classic 1234567890123456"),
                         "Visa Classic 123456**********3456")
        # Счёт
        self.assertEqual(mask_account_card("Счет 40817810999910000001"),
                         "Счет **************0001")

    def test_get_date(self):
        """Проверка правильного формата даты"""
        date_string = "2024-03-11T14:30:00Z"
        formatted_date = get_date(date_string)
        self.assertEqual(formatted_date, "11.03.2024")


if __name__ == '__main__':
    unittest.main()
