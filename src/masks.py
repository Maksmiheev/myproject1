from typing import Optional


def get_mask_card_number(card_number: str) -> str:
    """Возвращает замаскированный номер банковской карты."""

    first_part = card_number[:6]
    last_part = card_number[-4:]
    middle = "**"
    result = f"{first_part[:-2]} {middle} **** {last_part}"
    return result



