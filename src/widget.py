"""
Module for hiding personal bank data (account number and card number)
Additionally has function for making date formatting
"""

from datetime import datetime
from typing import Any

from src.masks import get_mask_account, get_mask_card_number

credit_card_names = ["visa", "maestro", "mastercard", "белкарт", "мир"]


def mask_account_card(bank_data: Any) -> str:
    """
    Masks personal bank data (account number and bank card number)

    Args:
        bank_data (str): personal bank data in (either bank account number or bank card number)
        in format 'Счет 73654108430135874305' or 'Visa Platinum 7000792289606361'

    Returns:
        str: masked personal bank data (account number and bank card number)
        or 'Invalid input' if validation fails (not string type given)

    Examples:
        Visa Platinum 7000792289606361 -> Visa Platinum 7000 79** **** 6361
        Счет 73654108430135874305 -> Счет **430
    """

    try:
        modified_bank_data = bank_data.strip().lower().split()
        if (
            modified_bank_data[0] in credit_card_names
            and len(modified_bank_data[-1]) == 16
            and modified_bank_data[-1].isdigit()
        ):
            card_number = modified_bank_data[-1]
            masked_card_number = get_mask_card_number(card_number)
            hidden_bank_data = f"{' '.join(modified_bank_data[:-1]).title()} {masked_card_number}"

        elif (
            modified_bank_data[0] in ("счет", "счёт")
            and len(modified_bank_data[-1]) == 20
            and modified_bank_data[-1].isdigit()
        ):
            bank_account_number = modified_bank_data[-1]
            masked_account_number = get_mask_account(bank_account_number)
            hidden_bank_data = f"{' '.join(modified_bank_data[:-1]).title()} {masked_account_number}"

        else:
            return "Invalid data given"

        return hidden_bank_data

    except Exception:
        return "Invalid input"


def get_date(date: str) -> str:
    """
    Using datetime module converts given datetime (ISO 8601) to DD.MM.YYYY format

    Args:
        date (str): date in format YYYY-MM-DDTHH:MM:SS.ssssss

    Returns:
        formatted_date (str) in format DD.MM.YYYY
        or 'Invalid date' if validation fails (not ISO-format or string type given)
    """

    try:
        formatted_date = datetime.fromisoformat(date).strftime("%d.%m.%Y")
        return formatted_date

    except ValueError:
        return "Invalid date"
