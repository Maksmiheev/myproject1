import unittest
from unittest.mock import patch, MagicMock
from src.external_api import process_transaction, load_environment_variables

class TestConvertCurrency(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api_response = MagicMock(status_code=200)
        cls.api_response.json.return_value = {'result': 6000.0}  # Предполагаемый результат конвертации

    @patch('requests.get')
    def test_process_transaction_usd_to_rub(self, mock_requests_get):
        """Проверка конвертации USD в RUB."""
        mock_requests_get.return_value = self.api_response
        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {
                    "code": "USD"
                }
            }
        }
        result = process_transaction(transaction)
        self.assertAlmostEqual(result, 6000.0)

    @patch('requests.get', side_effect=lambda *args, **kwargs: MagicMock(status_code=400))
    def test_process_transaction_api_error(self, mock_requests_get):
        """Проверка реакции на ошибку API."""
        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {
                    "code": "USD"
                }
            }
        }
        with self.assertRaises(Exception):
            process_transaction(transaction)

    def test_process_transaction_rub(self):
        """Проверка случая, когда валюта уже в рублях."""
        transaction = {
            "operationAmount": {
                "amount": "1000",
                "currency": {
                    "code": "RUB"
                }
            }
        }
        result = process_transaction(transaction)
        self.assertEqual(result, 1000.0)

    def test_process_transaction_missing_currency(self):
        """Проверка ситуации, когда валюта не задана."""
        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {}
            }
        }
        with self.assertRaises(ValueError):
            process_transaction(transaction)

    def test_load_environment_variables(self):
        """Проверка загрузки переменной окружения."""
        with patch.dict('os.environ', {"API_KEY_EXCHANGE_RATES_DATA": "fake-api-key"}):
            env_vars = load_environment_variables()
            self.assertIn("api_key", env_vars)
            self.assertEqual(env_vars["api_key"], "fake-api-key")

if __name__ == '__main__':
    unittest.main()
