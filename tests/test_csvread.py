import unittest
from io import StringIO
import tempfile
import os
import pandas as pd
from openpyxl import Workbook
from src.csvread import (read_financial_csv,read_financial_xlsx)

class TestFinancialFileReading(unittest.TestCase):

    def setUp(self):
        self.test_data = [
            {"Date": "2023-01-01", "Amount": 100},
            {"Date": "2023-01-02", "Amount": 200}
        ]

    def test_read_valid_csv_file(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".csv") as temp_csv:
            df = pd.DataFrame(self.test_data)
            df.to_csv(temp_csv.name, index=False)

            result = read_financial_csv(temp_csv.name)
            expected_result = self.test_data
            self.assertEqual(result, expected_result)

        os.unlink(temp_csv.name)

    def test_read_nonexistent_csv_file(self):
        non_existing_file = "/path/to/nonexistent.csv"
        result = read_financial_csv(non_existing_file)
        self.assertEqual(result, [])

    def test_read_empty_csv_file(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".csv") as empty_csv:
            pass  # Создаем пустой файл

            result = read_financial_csv(empty_csv.name)
            self.assertEqual(result, [])

        os.unlink(empty_csv.name)

    def test_read_valid_xlsx_file(self):
        with tempfile.NamedTemporaryFile(mode='wb+', delete=False, suffix=".xlsx") as temp_xlsx:
            df = pd.DataFrame(self.test_data)
            df.to_excel(temp_xlsx.name, index=False)

            result = read_financial_xlsx(temp_xlsx.name)
            expected_result = self.test_data
            self.assertEqual(result, expected_result)

        os.unlink(temp_xlsx.name)

    def test_read_nonexistent_xlsx_file(self):
        non_existing_file = "/path/to/nonexistent.xlsx"
        result = read_financial_xlsx(non_existing_file)
        self.assertEqual(result, [])

    def test_read_empty_xlsx_file(self):
        with tempfile.NamedTemporaryFile(mode='wb+', delete=False, suffix=".xlsx") as empty_xlsx:
            wb = Workbook()
            ws = wb.active
            wb.save(empty_xlsx.name)

            result = read_financial_xlsx(empty_xlsx.name)
            self.assertEqual(result, [])  # Пустой файл вернет пустой список

        os.unlink(empty_xlsx.name)


if __name__ == '__main__':
    unittest.main()