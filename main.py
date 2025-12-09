import os
import re
from collections import Counter
import json
import csv
import openpyxl
from datetime import datetime


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Выполняет поиск операций по ключевому слову в описании.

    :param data: Список банковских операций
    :param search: Критерий поиска (регулярное выражение)
    :return: Найденный список операций
    """
    pattern = re.compile(search, re.IGNORECASE)
    return [item for item in data if 'description' in item and pattern.search(item['description'])]


def process_bank_operations(data: list[dict], categories: list[str]) -> dict:
    """
    Производит подсчёт операций по указанным категориям.

    :param data: Список банковских операций
    :param categories: Категории для анализа
    :return: Словарь с числом операций по каждой категории
    """
    counter = Counter()
    for operation in data:
        description = operation.get('description', '')
        for category in categories:
            if category.lower() in description.lower():
                counter.update([category])
    return dict(counter)


# Загрузка данных из файлов
def load_json_data(file_path: str) -> list[dict]:
    """
    Читает данные из JSON-файла.

    :param file_path: Путь к файлу
    :return: Список объектов из JSON
    """
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)


def load_csv_data(file_path: str) -> list[dict]:
    """
    Читает данные из CSV-файла.

    :param file_path: Путь к файлу
    :return: Список словарей с данными из CSV
    """
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def load_xlsx_data(file_path: str) -> list[dict]:
    """
    Читает данные из XLSX-файла.

    :param file_path: Путь к файлу
    :return: Список словарей с данными из XLSX
    """
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    headers = [cell.value for cell in sheet[1]]
    rows = [[cell.value for cell in row] for row in sheet.iter_rows(min_row=2)]
    return [{headers[i]: val for i, val in enumerate(row)} for row in rows]


# Фильтрация операций по статусу
def filter_by_status(data: list[dict], status: str) -> list[dict]:
    """
    Отбирает операции по указанному статусу.

    :param data: Список операций
    :param status: Статус для фильтрации
    :return: Список операций нужного статуса
    """
    return [item for item in data if item.get('state', '').upper() == status.upper()]


# Сортировка операций по дате
def sort_by_date(data: list[dict], ascending: bool = True) -> list[dict]:
    """
    Сортирует операции по дате.

    :param data: Список операций
    :param ascending: Направление сортировки (True — восходящее, False — нисходящее)
    :return: Отсортированные операции
    """
    def extract_date(op):
        return datetime.strptime(op.get('date', ''), '%Y-%m-%dT%H:%M:%S.%f')
    return sorted(data, key=extract_date, reverse=not ascending)


# Форматирование вывода операций
def format_output(operation: dict) -> None:
    """
    Выводит одну операцию в удобочитаемом виде.

    :param operation: Объект операции
    """
    date = datetime.strptime(operation.get('date', ''), '%Y-%m-%dT%H:%M:%S.%f')
    formatted_date = date.strftime('%d.%m.%Y')
    from_account = operation.get('from', '').replace('*', '')[-4:] or '-'
    to_account = operation.get('to', '').replace('*', '')[-4:] or '-'
    amount = float(operation.get('operationAmount', {}).get('amount', 0))
    currency = operation.get('operationAmount', {}).get('currency', {}).get('code', '')
    print(f"{formatted_date} {operation.get('description', '')}")
    print(f"Счёт отправителя: {from_account} → счёт получателя: {to_account}")
    print(f"Сумма: {amount:.2f} {currency}\n")


# Основная программа
def main():
    """
    Запускает основную работу программы.
    Осуществляет загрузку данных, фильтр операций по статусу,
    производит дополнительные запросы и выводит итоговую статистику.
    """
    print("Программа обработки банковских транзакций.\n")

    # Предполагается единственность файла в директории 'data'.
    directory = './data/'
    files = os.listdir(directory)
    if len(files) != 1:
        print("Ошибка: количество файлов в каталоге отличается от одного.")
        return

    file_name = files[0]
    full_file_path = os.path.join(directory, file_name)

    # Определяем расширение файла
    extension = file_name.split('.')[-1].lower()
    if extension == 'json':
        data = load_json_data(full_file_path)
    elif extension == 'csv':
        data = load_csv_data(full_file_path)
    elif extension == 'xlsx':
        data = load_xlsx_data(full_file_path)
    else:
        print("Неподдерживаемый формат файла.")
        return

    # Выбираем статус операций для анализа
    available_statuses = ["EXECUTED", "CANCELED"]
    status = input(f"Введите нужный статус ({', '.join(available_statuses)}): ").strip().upper()
    while status not in available_statuses:
        print("Некорректный статус. Повторите ввод.")
        status = input(f"Введите нужный статус ({', '.join(available_statuses)}): ").strip().upper()

    # Фильтруем и сортируем данные
    filtered_data = filter_by_status(data, status)
    sorted_data = sort_by_date(filtered_data)

    # Печать операций
    print(f"\nОтобранные операции с статусом '{status}'\n")
    for op in sorted_data:
        format_output(op)

    # Дополнительный поиск операций
    if input("\nХотите дополнительно провести поиск среди операций? (y/n): ").strip().lower() == 'y':
        search_query = input("Введите строку для поиска в описаниях операций: ")
        found_ops = process_bank_search(sorted_data, search_query)
        if found_ops:
            print("\nНайдено по вашему запросу:\n")
            for op in found_ops:
                format_output(op)
        else:
            print("\nПо вашему запросу ничего не найдено.")

    # Итоговая статистика по операциям
    categories = ["Оплата услуг", "Переводы", "Покупки"]  # Примеры возможных категорий
    statistics = process_bank_operations(filtered_data, categories)
    print("\nИтоговая статистика по категориям операций:")
    for cat, count in statistics.items():
        print(f"- {cat}: {count} операция(-и)")


if __name__ == "__main__":
    main()
