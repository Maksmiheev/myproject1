import requests
from dotenv import load_dotenv
import os


def load_environment_variables(env_file=".env"):
    """Загружает переменные окружения из .env"""
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

    details = transaction.get('details', {})
    amount = details.get('amount')
    currency = details.get('currency').upper() if details.get('currency') else None

    if not isinstance(amount, (float, int)) or amount <= 0:
        raise ValueError("Некорректная сумма транзакции.")

    if currency is None or currency.strip() == '':
        raise ValueError("Отсутствует валюта транзакции.")

    return amount





























