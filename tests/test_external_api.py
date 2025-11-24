import unittest
from unittest.mock import patch, MagicMock
import requests
from external_api import (convert_currency, process_transaction,load_environment_variables)


class TestCurrencyConversion(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.env_vars = load_environment_variables()  # Загрузка реальных переменных среды перед началом тестов

    @patch('requests.get')
    def test_convert_currency_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'rates': {'RUB': 80}}  # Тестируемый обменный курс USD->RUB
        mock_get.return_value = mock_response

        result = convert_currency(100, 'USD', 'RUB')  # Запрашиваем конвертацию 100 долларов в рубли
        self.assertEqual(result, 8000.00)  # Ожидаемый результат: 100*80 = 8000 рублей

    @patch('requests.get')
    def test_convert_currency_connection_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response

        with self.assertRaises(ConnectionError):
            convert_currency(100, 'USD', 'RUB')

    @patch('requests.get')
    def test_convert_currency_unknown_currency(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'rates': {}}
        mock_get.return_value = mock_response

        with self.assertRaises(KeyError):
            convert_currency(100, 'USD', 'XXX')  # Валюта XXX не существует

    def test_process_transaction_rub(self):
        transaction = {'amount': 1000, 'currency': 'RUB'}
        result = process_transaction(transaction)
        self.assertEqual(result, 1000)

    @patch('your_module.convert_currency')
    def test_process_transaction_usd(self, mock_convert):
        mock_convert.return_value = 8000
        transaction = {'amount': 100, 'currency': 'USD'}
        result = process_transaction(transaction)
        self.assertEqual(result, 8000)

    @patch('your_module.convert_currency')
    def test_process_transaction_eur(self, mock_convert):
        mock_convert.return_value = 9000
        transaction = {'amount': 100, 'currency': 'EUR'}
        result = process_transaction(transaction)
        self.assertEqual(result, 9000)

    def test_process_transaction_invalid_currency(self):
        transaction = {'amount': 100, 'currency': 'XYZ'}
        with self.assertRaises(ValueError):
            process_transaction(transaction)


if __name__ == '__main__':
    unittest.main()