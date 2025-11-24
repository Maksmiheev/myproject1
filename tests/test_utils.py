import unittest
from unittest.mock import patch, mock_open, call
from pathlib import Path
from src.utils import load_financial_transactions

class TestLoadFinancialTransactions(unittest.TestCase):
    def test_load_valid_json(self):
        valid_json_content = '[{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]'
        expected_result = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]

        with patch('builtins.open', mock_open(read_data=valid_json_content)):
            result = load_financial_transactions()
            self.assertEqual(result, expected_result)

    def test_empty_file(self):
        empty_json_content = ''
        expected_result = []

        with patch('builtins.open', mock_open(read_data=empty_json_content)):
            result = load_financial_transactions()
            self.assertEqual(result, expected_result)

    def test_non_list_json(self):
        invalid_json_content = '{"key": "value"}'  # Содержит словарь, а не список
        expected_result = []

        with patch('builtins.open', mock_open(read_data=invalid_json_content)):
            result = load_financial_transactions()
            self.assertEqual(result, expected_result)

    def test_file_not_found(self):
        file_path = '/nonexistent/path/to/file.json'
        expected_result = []

        with patch('pathlib.Path.exists', return_value=False):
            result = load_financial_transactions(file_path)
            self.assertEqual(result, expected_result)

    def test_unexpected_exception(self):
        error_message = "Some unexpected exception occurred."
        expected_result = []

        with patch('builtins.open', side_effect=Exception(error_message)):
            result = load_financial_transactions()
            self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()