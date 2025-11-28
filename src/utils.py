import json
from typing import List, Dict
import logging
from datetime import datetime


logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)


log_format = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
formatter = logging.Formatter(log_format)


current_date = datetime.now().strftime('%Y-%m-%d_%H%M%S')
file_handler = logging.FileHandler(f'./logs/{current_date}_utils.log', mode='w')  # Перезаписываем файл при каждом запуске
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)


def load_financial_transactions(file_path: str = 'data/operations.json') -> List[Dict]:
    """
    Загружает финансовые транзакции из заданного JSON-файла.
    """
    try:
        with open(file_path, encoding='utf-8') as f:

            content = f.read()

        if not content.strip():
            logger.warning(f"Содержимое файла '{file_path}' пустое")
            return []

        transactions = json.loads(content)

        if isinstance(transactions, list):
            logger.info(f"Успешно загружено {len(transactions)} финансовых транзакций из файла '{file_path}'.")
            return transactions
        else:
            logger.error(f"Файл '{file_path}' содержит некорректный формат данных.")
            return []

    except FileNotFoundError:
        logger.error(f"Ошибка: файл '{file_path}' не найден.")
        return []
    except json.JSONDecodeError:
        logger.error(f"Ошибка: неверный формат JSON-файла '{file_path}'.")
        return []
    except Exception as e:
        logger.error(f"Произошла ошибка при загрузке транзакций из файла '{file_path}': {e}.")
        return []