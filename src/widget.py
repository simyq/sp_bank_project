"""
Module for hiding personal bank data (account number and card number)
Additionally has function for making date formatting
"""

from datetime import datetime
from typing import Any

from masks import get_mask_account, get_mask_card_number

credit_card_names = ["visa", "maestro", "mastercard", "белкарт", "мир"]


def mask_account_card(bank_data: Any) -> str:
    """
        Masks personal bank data (account number and bank card number)

        Args:
            bank_data must be a string: personal bank data in (either bank account number or bank card number)
            in format 'Счет 73654108430135874305' or 'Visa Platinum 7000792289606361'

        Returns:
            str: masked personal bank data (account number and bank card number)
            or raises an Exception if validation fails
    """

    try:
        if not isinstance(bank_data, str):
            raise ValueError("Input must be a string")

        modified_bank_data = bank_data.strip().lower().split()
        if not modified_bank_data:
            raise ValueError("Empty input")

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
            raise ValueError("Input must be a string with 16 digits for card number and 20 digits for account number")

        return hidden_bank_data

    except ValueError as e:
        return f"Invalid input: {e}"

    except Exception:
        return "Unexpected error occurred"


def get_date(date: Any) -> str:
    """
    Using datetime module converts given datetime (ISO 8601) to DD.MM.YYYY format

    Args:
        date: must be a string: date in format YYYY-MM-DDTHH:MM:SS.ssssss
        if not, validation fails, Exception occurs

    Returns:
        formatted_date (str) in format DD.MM.YYYY
        or 'Invalid input' if validation fails (not ISO-format or string type given)
    """

    try:
        if not isinstance(date, str):
            raise TypeError
        else:
            formatted_date = datetime.fromisoformat(date).strftime("%d.%m.%Y")
            return formatted_date

    except (ValueError, AttributeError, TypeError):
        return "Invalid input: date must be a string in ISO-format"
