import os
import re
from collections import Counter
import json
import csv
import openpyxl
from datetime import datetime


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [item for item in data if pattern.search(item.get("description", ""))]



def process_bank_operations(data: list[dict], categories: list[str]) -> dict:
    descriptions = [item.get("description", "") for item in data]
    counts = Counter(descriptions)
    return {category: counts.get(category, 0) for category in categories}



def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def load_csv(path):
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def load_xlsx(path):
    wb = openpyxl.load_workbook(path)
    sheet = wb.active
    data = []
    headers = [cell.value for cell in next(sheet.rows)]
    for row in sheet.iter_rows(min_row=2):
        data.append({headers[i]: row[i].value for i in range(len(headers))})
    return data

def filter_status(data, status):
    status = status.upper()
    return [op for op in data if (op.get("status", "").upper() == status)]

def prompt_status():
    statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = input(f'Введите статус, по которому необходимо выполнить фильтрацию.\nДоступные для фильтрации статусы: {", ".join(statuses)}\n').strip().upper()
        if status in statuses:
            print(f'Операции отфильтрованы по статусу "{status}"')
            return status
        print(f'Статус операции "{status}" недоступен.')

def prompt_yes_no(message):
    while True:
        answer = input(message + " Да/Нет\n").strip().lower()
        if answer in ["да", "нет"]:
            return answer == "да"
        print("Пожалуйста, введите 'Да' или 'Нет'.")

def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input().strip()
        if choice == "1":
            print("Для обработки выбран JSON-файл.")
            data = load_json("data.json")  # Здесь можно запросить у пользователя путь к файлу
            break
        elif choice == "2":
            print("Для обработки выбран CSV-файл.")
            data = load_csv("data.csv")
            break
        elif choice == "3":
            print("Для обработки выбран XLSX-файл.")
            data = load_xlsx("data.xlsx")
            break
        else:
            print("Некорректный выбор. Пожалуйста, выберите 1, 2 или 3.")

    status = prompt_status()
    filtered_data = filter_status(data, status)

    if not filtered_data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    if prompt_yes_no("Отсортировать операции по дате?"):
        order = input("Отсортировать по возрастанию или по убыванию?\n").strip().lower()
        reverse = order == "по убыванию"
        filtered_data.sort(key=lambda x: x.get("date", ""), reverse=reverse)

    if prompt_yes_no("Выводить только рублевые транзакции?"):
        filtered_data = [op for op in filtered_data if op.get("amount_currency") == "руб."]

    if prompt_yes_no("Отфильтровать список транзакций по определенному слову в описании?"):
        search_word = input("Введите слово для поиска в описании:\n").strip()
        filtered_data = process_bank_search(filtered_data, search_word)

    if not filtered_data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print("Распечатываю итоговый список транзакций...\n")
    print(f"Всего банковских операций в выборке: {len(filtered_data)}\n")

    for op in filtered_data:
        date = op.get("date", "")
        description = op.get("description", "")
        amount_value = op.get("amount_value", "")
        amount_currency = op.get("amount_currency", "")
        info = op.get("info", "")
        print(f"{date} {description}")
        if info:
            print(info)
        print(f"Сумма: {amount_value} {amount_currency}\n")
