from typing import Any, Dict, List


def filter_by_state(data: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """принимает список словарей и опционально значение для ключа state и возвращает новый список словарей,
    содержащий только те словари, у которых ключ state соответствует указанному значению."""
    return [item for item in data if item.get("state") == state]


def sort_by_date(data: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """принимает список словарей и необязательный параметр, задающий порядок сортировки и возвращает новый список, отсортированный по дате"""
    return sorted(data, key=lambda x: x["date"], reverse=descending)
