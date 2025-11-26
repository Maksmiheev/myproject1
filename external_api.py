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
def convert_currency(amount: float, from_currency: str, to_currency: str = "RUB") -> float:
    """
    Конвертирует указанную сумму из одной валюты в другую, используя внешний API.
    """
    params = {"symbols": to_currency, "base": from_currency}
    response = requests.get(BASE_URL, headers=HEADERS, params=params)

    if response.status_code != 200:
        raise ConnectionError(response.text)

    rates = response.json().get("rates", {})
    rate_to_target_currency = rates.get(to_currency)

    if rate_to_target_currency is None:
        raise KeyError(f"Валюта '{to_currency}' не найдена в списке курсов.")

    converted_amount = amount * rate_to_target_currency
    return round(converted_amount, 2)


def process_transaction(transaction: dict) -> float:
    """
    Обрабатывает финансовую транзакцию и возвращает сумму в рублях.
    """
    amount = transaction['amount']
    currency = transaction['currency'].upper()

    if currency == "RUB":
        return amount
    elif currency in ["USD", "EUR"]:
        return convert_currency(amount, currency)
    else:
        raise ValueError(f"Транзакция выполнена в неизвестной валюте: {currency}.")





























