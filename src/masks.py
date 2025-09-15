"""
Module with functions for hiding personal bank data (credit card number and bank account)
"""

from typing import Any


def get_mask_card_number(card_number: Any) -> str:
    """
    Masks a credit card number for secure display.

    Args:
        card_number: Credit card number as integer (16 digits)

    Returns:
         hidden card number in 'XXXX XX** **** XXXX' format (string) or 'Invalid Input' if validation fails
    """

    if isinstance(card_number, int) and len(str(card_number)) == 16:
        masked_card_number = f"{str(card_number)[:4]} {str(card_number)[4:6]}** **** {str(card_number)[-4:]}"

        return masked_card_number

    return "Invalid Input"


def get_mask_account(account_number: Any) -> str:
    """
    Masks bank account number for secure display.

    Args:
        account_number: Bank account number as integer (20 digits)

    Returns:
         hidden account number in '**XXXX' format (string) or 'Invalid Input' if validation fails
    """

    if isinstance(account_number, int) and len(str(account_number)) == 20:
        masked_account_number = f"**{str(account_number)[-4:]}"

        return masked_account_number

    return "Invalid Input"
