import logging
from datetime import datetime

LOG_FILE_PATH = "logs/loghome.log"

log_format = "%(asctime)s - %(name)s - %(levelname)s: %(message)s"


logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)
current_date = datetime.now().strftime("%Y-%m-%d_%H%M%S")
file_handler = logging.FileHandler(f"./logs/loghome.log", mode="w")  # 'w' режим перезаписи файла
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    try:
        first_part = card_number[:6]
        last_part = card_number[-4:]
        middle = "**"
        result = f"{first_part[:-2]} {middle} **** {last_part}"

        # Запись успешного результата операции в лог
        logger.debug(f"Карточный номер успешно замаскирован: {result}")
        return result

    except Exception as e:
        # Запись ошибки в лог
        logger.error(f"Ошибка при маскировке номера карточки: {card_number}, ошибка: {str(e)}")
        raise


def get_mask_account(account_number: str) -> str:
    try:
        if len(account_number) < 4 or not account_number.isdigit():
            raise ValueError("Номер счета должен содержать минимум 4 цифры.")

        masked_account = f"**{account_number[-4:]}"

        # Запись успешного результата операции в лог
        logger.debug(f"Банковский счёт успешно замаскирован: {masked_account}")
        return masked_account

    except Exception as e:
        # Запись ошибки в лог
        logger.error(f"Ошибка при маскировке банковского счёта: {account_number}, ошибка: {str(e)}")
        raise
