"""
Module with functions for hiding personal bank data (credit card number and bank account)
"""


def get_mask_card_number(card_number: str) -> str:
    """
    Masks a credit card number for secure display.

    Args:
        card_number: Credit card number as string (16 digits)

    Returns:
         hidden card number in 'XXXX XX** **** XXXX' format (string)
    """

    masked_card_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"

    return masked_card_number


def get_mask_account(account_number: str) -> str:
    """
    Masks bank account number for secure display.

    Args:
        account_number: Bank account number as string (20 digits)

    Returns:
         hidden account number in '**XXXX' format (string)
    """

    masked_account_number = f"**{str(account_number)[-4:]}"

    return masked_account_number
