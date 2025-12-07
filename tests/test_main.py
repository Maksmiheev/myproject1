import unittest
from datetime import datetime

from main import (filter_by_status, process_bank_operations,
                  process_bank_search, sort_by_date)


class TestBankFunctions(unittest.TestCase):

    def setUp(self):
        self.data = [
            {
                "id": 1,
                "state": "EXECUTED",
                "date": "2019-12-08T17:15:00.000+03:00",
                "description": "Открытие вклада",
                "from": "Счет **4321",
                "to": "",
                "operationAmount": {"amount": "40542", "currency": {"code": "RUB"}},
            },
            {
                "id": 2,
                "state": "EXECUTED",
                "date": "2019-11-12T15:30:00.000+03:00",
                "description": "Перевод с карты на карту",
                "from": "MasterCard 7771 27** **** 3727",
                "to": "Visa Platinum 1293 38** **** 9203",
                "operationAmount": {"amount": "130", "currency": {"code": "USD"}},
            },
            {
                "id": 3,
                "state": "CANCELED",
                "date": "2018-07-18T10:45:00.000+03:00",
                "description": "Перевод организации",
                "from": "Visa Platinum 7492 65** **** 7202",
                "to": "Счет **0034",
                "operationAmount": {"amount": "8390", "currency": {"code": "RUB"}},
            },
        ]

    def test_process_bank_search(self):
        # Проверяем, что ищем совпадения в описании операций
        result = process_bank_search(self.data, "Открытие")
        expected_result = [self.data[0]]
        self.assertEqual(result, expected_result)

        # Поиск слова, которого нет в списке операций
        result = process_bank_search(self.data, "Депозит")
        expected_result = []
        self.assertEqual(result, expected_result)

    def test_process_bank_operations(self):
        # Проверяем категоризацию операций
        categories = ["Открытие", "Перевод"]
        result = process_bank_operations(self.data, categories)
        expected_result = {"Открытие": 1, "Перевод": 2}
        self.assertDictEqual(result, expected_result)

    def test_filter_by_status(self):
        # Проверяем фильтрацию по статусу
        result = filter_by_status(self.data, "EXECUTED")
        expected_result = [self.data[0], self.data[1]]
        self.assertListEqual(result, expected_result)

        # Проверяем случай отсутствия указанного статуса
        result = filter_by_status(self.data, "TEST_STATUS")
        expected_result = []
        self.assertListEqual(result, expected_result)

    def test_sort_by_date(self):
        # Сортируем операции по дате по возрастанию
        sorted_data = sort_by_date(self.data, ascending=True)
        dates = [datetime.strptime(op["date"], "%Y-%m-%dT%H:%M:%S.%f") for op in sorted_data]
        self.assertTrue(
            all(dates[i] <= dates[i + 1] for i in range(len(dates) - 1)), "Даты не отсортированы по возрастанию"
        )

        # Сортируем операции по дате по убыванию
        sorted_data_descending = sort_by_date(self.data, ascending=False)
        dates_descending = [datetime.strptime(op["date"], "%Y-%m-%dT%H:%M:%S.%f") for op in sorted_data_descending]
        self.assertTrue(
            all(dates_descending[i] >= dates_descending[i + 1] for i in range(len(dates_descending) - 1)),
            "Даты не отсортированы по убыванию",
        )


if __name__ == "__main__":
    unittest.main()
