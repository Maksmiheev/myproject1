from typing import Optional


def get_mask_card_number(card_number: str) -> str:
    """Возвращает замаскированный номер банковской карты."""

    first_part = card_number[:6]
    last_part = card_number[-4:]
    middle = "**"
    result = f"{first_part[:-2]} {middle} **** {last_part}"
    return result


def get_mask_account(account_number: str) -> str:
    """Возвращает замаскированный банковский счет в формате **XXXX."""

    if len(account_number) < 4 or not account_number.isdigit():
        raise ValueError("Номер счета должен содержать минимум 4 цифры.")

    return f"**{account_number[-4:]}"
