Проект BankProject

## Описание:
Этот проект содержит набор функций для работы с банковскими данными и списками транзакций: маскировка номеров карт и счетов, фильтрация и сортировка данных по дате и состоянию.
## Установка:
1. Клонируйте репозиторий:
```
https://github.com/Maksmiheev/myproject1.git
```
2.Установите зависимости:
```
pip install -r requirements.txt
```
## Использование:
Этот проект позволяет безопасно работать с банковскими данными, маскируя номера карт и счетов, форматируя дату и фильтруя транзакции по состоянию, а так же быстро и удобно находить нужную информацию о транзакциях и проводить анализ данных. Так же обновлен функционал , реализована функция считывания финансовых операций из CSV- и XLSX-файлов, позволяющая пользователю выбрать интересующие его транзакции.

- Импортируйте необходимые функции из модуля.
- Используйте `mask_card` и `mask_account` для маскировки номеров.
- Преобразуйте даты в удобочитаемый формат с помощью `get_date`.
- Фильтруйте и сортируйте данные транзакций посредством `filter_by_state` и `sort_by_date`.
- Работайте с массивами транзакций с помощью функций `filter_by_currency`, `transaction_descriptions` и `card_number_generator`.
- Получайте информацию о транзакциях из JSON, CSV и XLSX-файлов с помощью функций `read_financial_csv`, `read_financial_xlsx` и целового модуля main.


Пример:

```python
from ваш_модуль import mask_account_card, get_date, filter_by_state, sort_by_date

data = [
    {"state": "EXECUTED", "date": "2024-03-11T10:20:30", "account": "40817810099910004312"},
    {"state": "PENDING", "date": "2024-03-10T15:10:20", "account": "12345678901234567890"},
]

filtered = filter_by_state(data)
sorted_data = sort_by_date(filtered)

for item in sorted_data:
    print(get_date(item["date"]), mask_account_card(f"Счет {item['account']}"))
```
Пример работы с JSON, CSV и XLSX-файлами с помощью функций `read_financial_csv`, `read_financial_xlsx`
``` 
csv_file_path = 'finances.csv'
operations_from_csv = read_financial_csv(csv_file_path)
print("Операции из CSV:", operations_from_csv[:3])  # вывод первых трех операций

xlsx_file_path = 'finances.xlsx'
operations_from_xlsx = read_financial_xlsx(xlsx_file_path)
print("Операции из XLSX:", operations_from_xlsx[:3])  # вывод первых трех операций
```

## Тестирование: 
Добавлено тестирование функций во всех модулях программы для выявления некорректной работоспособности программы в различных кейсах.

## Документация:

Дополнительную информацию о структуре проекта и API можно найти в [документации](README.md).
