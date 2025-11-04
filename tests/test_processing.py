import unittest
from typing import List, Dict, Any


def filter_by_state(data: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """Фильтрует список словарей по заданному состоянию."""
    return [item for item in data if item.get('state') == state]


class TestFilterByState(unittest.TestCase):
    def setUp(self):
        self.test_data = [
            {'id': 1, 'state': 'EXECUTED'},
            {'id': 2, 'state': 'CANCELED'},
            {'id': 3, 'state': 'EXECUTED'}
        ]

    def test_filter_executed(self):
        """Тест базового функционала фильтрации по EXECUTED."""
        filtered = filter_by_state(self.test_data)
        self.assertEqual(len(filtered), 2)
        self.assertIn({'id': 1, 'state': 'EXECUTED'}, filtered)
        self.assertIn({'id': 3, 'state': 'EXECUTED'}, filtered)

    def test_filter_canceled(self):
        """Тест фильтрации по CANCELED."""
        filtered = filter_by_state(self.test_data, 'CANCELED')
        self.assertEqual(len(filtered), 1)
        self.assertIn({'id': 2, 'state': 'CANCELED'}, filtered)

    def test_no_matching_state(self):
        """Тест реакции на состояние, которого нет в списке."""
        filtered = filter_by_state(self.test_data, 'PENDING')
        self.assertEqual(filtered, [])

if __name__ == '__main__':
    unittest.main()

def sort_by_date(data: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """Отсортировать список словарей по полю 'date'. По умолчанию сортировка идет в обратном порядке."""
    return sorted(data, key=lambda x: x['date'], reverse=descending)

class TestSortByDate(unittest.TestCase):
    def setUp(self):
        # Исходные данные для тестов
        self.data = [
            {"id": 1, "date": "2023-01-01"},
            {"id": 2, "date": "2023-01-03"},
            {"id": 3, "date": "2023-01-02"}
        ]

    def test_sort_descending(self):
        """Тест на сортировку по убыванию (default mode)."""
        sorted_data = sort_by_date(self.data)
        expected_order = ["2023-01-03", "2023-01-02", "2023-01-01"]
        dates = [item["date"] for item in sorted_data]
        self.assertListEqual(dates, expected_order)

    def test_sort_ascending(self):
        """Тест на сортировку по возрастанию."""
        sorted_data = sort_by_date(self.data, descending=False)
        expected_order = ["2023-01-01", "2023-01-02", "2023-01-03"]
        dates = [item["date"] for item in sorted_data]
        self.assertListEqual(dates, expected_order)

if __name__ == '__main__':
    unittest.main()


