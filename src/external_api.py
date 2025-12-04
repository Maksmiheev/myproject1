import json
import os

import requests
from dotenv import load_dotenv


def load_environment_variables():
    """
    Загружает переменные окружения из .env файла.
    """
    load_dotenv()

    api_key_exchange_rates_data = os.getenv("API_KEY_EXCHANGE_RATES_DATA")

    if not api_key_exchange_rates_data:
        raise ValueError("Переменная API_KEY_EXCHANGE_RATES_DATA отсутствует в файле .env!")

    return {"api_key": api_key_exchange_rates_data}


env_vars = load_environment_variables()
API_KEY = env_vars["api_key"]
BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"
HEADERS = {"apikey": API_KEY}


def process_transaction(transaction: dict) -> float:
    """
    Обрабатывает финансовую транзакцию и возвращает сумму в рублях.
    """

    amount_value = transaction.get("operationAmount", {}).get("amount")
    if not isinstance(amount_value, str):
        raise ValueError("Сумма транзакции указана некорректно.")

    amount_value = float(amount_value.replace(",", "."))

    if amount_value <= 0:
        raise ValueError("Некорректная сумма транзакции.")

    # Извлекаем код валюты
    currency_code = transaction.get("operationAmount", {}).get("currency", {}).get("code")

    if currency_code is None or currency_code.strip() == "":
        raise ValueError("Отсутствует валюта транзакции.")

    # Если валюта уже рубли, ничего конвертировать не надо
    if currency_code.upper() == "RUB":
        return amount_value

    # Если валюта отличается от поддерживаемых (USD/EUR), возвращаем None
    if currency_code.upper() not in {"USD", "EUR"}:
        return None

    # Конвертируем валюту через API
    params = {"from": currency_code.upper(), "to": "RUB", "amount": amount_value}

    response = requests.get(BASE_URL, headers=HEADERS, params=params)

    if response.status_code != 200:
        raise Exception(f"Ошибка при запросе к API: {response.text}")

    data = response.json()
    converted_amount = data.get("result")

    return converted_amount


if __name__ == "__main__":

    file_path = os.path.join(os.path.dirname(__file__), "../data/operations.json")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            transactions = json.load(file)
    except FileNotFoundError:
        print("Файл operations.json не найден.")
        exit()

    for i, transaction in enumerate(transactions[:5]):
        try:
            result = process_transaction(transaction)

            if result is not None:
                print(
                    f"Транзакция №{i + 1}: Получено {transaction['operationAmount']['amount']} "
                    f"{transaction['operationAmount']['currency']['code'].upper()}, эквивалентно {result:.2f} рублей."
                )
            elif result == 0:
                print(f"Транзакция №{i + 1}: Сумма была введена неверно.")
            else:
                print(
                    f"Транзакция №{i + 1}: Валюта '{transaction['operationAmount']['currency']['code']}' не поддерживается."
                )

        except Exception as e:
            print(f"Ошибка обработки транзакции №{i + 1}: {e}")
