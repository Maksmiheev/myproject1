import unittest
from unittest.mock import MagicMock, patch
from src import external_api


class TestProcessTransaction(unittest.TestCase):
    def setUp(self):
        self.valid_usd_transaction = {
            "operationAmount": {"amount": "100.00", "currency": {"code": "USD"}},
        }
        self.invalid_currency_transaction = {
            "operationAmount": {"amount": "100.00", "currency": {"code": "GBP"}},
        }
        self.rub_transaction = {
            "operationAmount": {"amount": "100.00", "currency": {"code": "RUB"}},
        }
        self.invalid_amount_transaction = {
            "operationAmount": {"amount": "-100.00", "currency": {"code": "USD"}},
        }

    @patch("requests.get")
    def test_valid_usd_transaction(self, mock_get):
        """Тестирует успешную конверсию из долларов"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 7500.00}  # Предположим, курс примерно такой
        mock_get.return_value = mock_response

        result = external_api.process_transaction(self.valid_usd_transaction)
        self.assertEqual(result, 7500.00)

    @patch("requests.get")
    def test_invalid_currency(self, mock_get):
        """Тестирует неподдерживаемую валюту"""
        result = external_api.process_transaction(self.invalid_currency_transaction)
        self.assertIsNone(result)

    def test_rub_transaction(self):
        """Тестирует случай, когда валюта уже в рублях"""
        result = external_api.process_transaction(self.rub_transaction)
        self.assertEqual(result, 100.00)

    def test_invalid_amount(self):
        """Тестирует ошибку при отрицательной сумме"""
        with self.assertRaises(ValueError):
            external_api.process_transaction(self.invalid_amount_transaction)

    @patch("requests.get")
    def test_api_error(self, mock_get):

        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_get.return_value = mock_response

        with self.assertRaises(Exception):
            external_api.process_transaction(self.valid_usd_transaction)


if __name__ == "__main__":
    unittest.main()
