from datetime import datetime

def mask_card(number: str) -> str:
    """Маскирует карту следующим образом: первые 6 и последние 4 цифры видны, остальные заменены *"""
    return number[:6] + "*" * (len(number) - 10) + number[-4:]

def mask_account(number: str) -> str:
    """Маскирует счет, показывая только последние 4 цифры"""
    return "*" * (len(number) - 4) + number[-4:]

def mask_account_card(input_str: str) -> str:
    """Маскирует счет, показывая только последние 4 цифры"""
    parts = input_str.split()
    """Номер всегда последний элемент"""
    number = parts[-1]
    """Имя — все до номера"""
    name = " ".join(parts[:-1])

    if name.lower().startswith("счет"):
        masked_number = mask_account(number)
    else:
        masked_number = mask_card(number)

    return f"{name} {masked_number}"


