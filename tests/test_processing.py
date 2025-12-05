import unittest
from src.processing import filter_by_state, sort_by_date


class TestOperations(unittest.TestCase):

    def setUp(self):
        # Примеры данных для тестирования
        self.data = [
            {"id": 1, "state": "EXECUTED", "date": "2023-05-01"},
            {"id": 2, "state": "CANCELED", "date": "2023-04-15"},
            {"id": 3, "state": "EXECUTED", "date": "2023-04-30"}
        ]

    def test_filter_by_state_default(self):
        """Тестирование фильтра по умолчанию (используя состояние EXECUTED)"""
        filtered = filter_by_state(self.data)
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(item["state"] == "EXECUTED" for item in filtered))

    def test_filter_by_state_custom(self):
        """Тестирование фильтра с другим состоянием (CANCELED)"""
        filtered = filter_by_state(self.data, state="CANCELED")
        self.assertEqual(len(filtered), 1)
        self.assertTrue(all(item["state"] == "CANCELED" for item in filtered))

    def test_sort_by_date_descending(self):
        """Тестирование сортировки по дате по убыванию"""
        sorted_data = sort_by_date(self.data)
        dates = [item["date"] for item in sorted_data]
        self.assertListEqual(dates, ["2023-05-01", "2023-04-30", "2023-04-15"])

    def test_sort_by_date_ascending(self):
        """Тестирование сортировки по дате по возрастанию"""
        sorted_data = sort_by_date(self.data, descending=False)
        dates = [item["date"] for item in sorted_data]
        self.assertListEqual(dates, ["2023-04-15", "2023-04-30", "2023-05-01"])


if __name__ == '__main__':
    unittest.main()
