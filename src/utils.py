import json
from typing import List, Dict


def load_financial_transactions(file_path: str = 'data/operations.json') -> List[Dict]:
    """
    Загружает финансовые транзакции из заданного JSON-файла.
    """
    try:
        with open(file_path, encoding='utf-8') as f:
            # Читаем содержимое файла
            content = f.read()

        if not content.strip():
            return []


        transactions = json.loads(content)


        if isinstance(transactions, list):
            return transactions
        else:
            return []

    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден.")
        return []
    except json.JSONDecodeError:
        print("Ошибка: неверный формат JSON-файла.")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []