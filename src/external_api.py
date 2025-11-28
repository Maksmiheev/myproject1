import os
import json
import requests
from dotenv import load_dotenv


def load_environment_variables(env_file="../.env"):
    """
    Загружает переменные окружения из .env.
    """
    load_dotenv(dotenv_path=env_file)

    api_key_exchange_rates_data = os.getenv("API_KEY_EXCHANGE_RATES_DATA")
    if not api_key_exchange_rates_data:
        raise ValueError("Переменная API_KEY_EXCHANGE_RATES_DATA отсутствует в .env!")

    return {
        "api_key": api_key_exchange_rates_data
    }


env_vars = load_environment_variables()
API_KEY = env_vars["api_key"]
BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"
HEADERS = {"apikey": API_KEY}


def process_transaction(transaction: dict) -> float:
    """
    Обрабатывает финансовую транзакцию и возвращает сумму в рублях.
    """
    amount = transaction.get('amount')
    currency = transaction.get('currency').upper() if transaction.get('currency') else None

    if not isinstance(amount, (float, int)) or amount <= 0:
        raise ValueError("Некорректная сумма транзакции.")

    if currency is None or currency.strip() == '':
        raise ValueError("Отсутствует валюта транзакции.")


    params = {
        "from": currency,
        "to": "RUB",
        "amount": amount
    }

    response = requests.get(BASE_URL, headers=HEADERS, params=params)

    if response.status_code != 200:
        raise Exception(f"Ошибка при запросе к API: {response.text}")

    data = response.json()
    converted_amount = data.get("result")

    return converted_amount


if __name__ == "__main__":

    with open("../operations.json", "r") as file:
        transactions = json.load(file)

    for i, transaction in enumerate(transactions[:5]):
        try:
            result = process_transaction(transaction)
            print(f"Транзакция №{i+1}: Получено {transaction['amount']} {transaction['currency']}, эквивалентно {result:.2f} рублей.")
        except Exception as e:
            print(f"Ошибка обработки транзакции №{i+1}: {e}")





























