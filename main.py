import re
from collections import defaultdict
import json
import csv
import openpyxl
from datetime import datetime


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    pattern = re.compile(search, re.IGNORECASE)

    result = []
    for item in data:
        if 'description' in item and pattern.search(item['description']):
            result.append(item)

    return result


def process_bank_operations(data: list[dict], categories: list[str]) -> dict:
    operations_count = defaultdict(int)

    for operation in data:
        description = operation.get('description', '')

        # Подсчет количества операций в заданных категориях
        for category in categories:
            if category.lower() in description.lower():
                operations_count[category] += 1

    return dict(operations_count)


# Функции чтения файлов
def load_json_data(file_path):
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)


def load_csv_data(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def load_xlsx_data(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    headers = [cell.value for cell in sheet[1]]
    rows = [[cell.value for cell in row] for row in sheet.iter_rows(min_row=2)]
    return [{headers[i]: val for i, val in enumerate(row)} for row in rows]


# Фильтрация операций по состоянию
def filter_by_status(data, status):
    filtered_data = [item for item in data if item.get('state').upper() == status.upper()]
    return filtered_data


# Сортировка операций по дате
def sort_by_date(data, ascending=True):
    sorted_data = sorted(data, key=lambda x: datetime.strptime(x.get('date'), '%Y-%m-%dT%H:%M:%S.%f'), reverse=not ascending)
    return sorted_data


# Форматирование вывода операций
def format_output(operation):
    date = datetime.strptime(operation.get('date'), '%Y-%m-%dT%H:%M:%S.%f')
    formatted_date = date.strftime('%d.%m.%Y')
    from_account = operation.get('from', '').replace('*', '')[-4:]
    to_account = operation.get('to', '').replace('*', '')[-4:]
    amount = float(operation.get('operationAmount', {}).get('amount'))
    currency = operation.get('operationAmount', {}).get('currency', {})
    currency_code = currency.get('code', '')
    print(f"{formatted_date} {operation.get('description')}")
    print(f"Счет {from_account} -> Счет {to_account}")
    print(f"Сумма: {amount:.2f} {currency_code}\n")


# Основная логика программы
def main():
    global data
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input()
    file_type = None
    while not file_type:
        try:
            if int(choice) == 1:
                file_type = 'json'
            elif int(choice) == 2:
                file_type = 'csv'
            elif int(choice) == 3:
                file_type = 'xlsx'
            else:
                raise ValueError
        except ValueError:
            print("Неверный выбор пункта меню!")
            choice = input()

    filename = input("Введите путь к файлу: ")

    # Загрузка данных в зависимости от типа файла
    if file_type == 'json':
        data = load_json_data(filename)
    elif file_type == 'csv':
        data = load_csv_data(filename)
    elif file_type == 'xlsx':
        data = load_xlsx_data(filename)

    # Выбор статуса операций
    available_statuses = ['EXECUTED', 'CANCELED', 'PENDING']
    status = ''
    while status.upper() not in available_statuses:
        status = input("Введите статус, по которому необходимо выполнить фильтрацию.\n"
                       "Доступные для фильтровки статусы: {}\n".format(', '.join(available_statuses)))

    # Фильтруем операции по введённому статусу
    filtered_data = filter_by_status(data, status)

    # Далее уточняем дальнейшие условия сортировки и фильтрации
    need_sort = input("Отсортировать операции по дате? Да/Нет\n").strip().lower() == 'да'
    if need_sort:
        order = input("Отсортировать по возрастанию или по убыванию?\n").strip().lower()
        ascending = True if order == 'по возрастанию' else False
        filtered_data = sort_by_date(filtered_data, ascending)

    rub_only = input("Выводить только рублевые транзакции? Да/Нет\n").strip().lower() == 'да'
    if rub_only:
        filtered_data = [op for op in filtered_data if op.get('operationAmount', {}).get('currency', {}).get('code') == 'RUB']

    word_filter = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n").strip().lower() == 'да'
    if word_filter:
        search_word = input("Введите слово для поиска:\n")
        filtered_data = process_bank_search(filtered_data, search_word)

    # Вывод результатов
    if len(filtered_data) > 0:
        print("\nВсего банковских операций в выборке:", len(filtered_data))
        for idx, transaction in enumerate(filtered_data):
            print(f"\nОперация №{idx + 1}:")
            format_output(transaction)
    else:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")


if __name__ == "__main__":
    main()
