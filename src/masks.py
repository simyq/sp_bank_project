"""
Module with functions for hiding personal bank data (credit card number and bank account)
"""

import logging
from typing import Any, Optional

from config import get_log_path

logger = logging.getLogger("utils_logger")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(filename=get_log_path("masks.log"), mode="w", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s: %(filename)s: %(levelname)s: %(message)s", datefmt="%d-%m-%Y %I:%M:%S")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

message_empty_string = "{}. Returning an empty string"


def get_mask_card_number(card_number: Optional[Any] = None) -> str:
    """
    Masks a credit card number for secure display.

    Args:
        card_number: Credit card number as string (16 digits)

    Returns:
         masked_card_number: hidden card number in 'XXXX XX** **** XXXX' format (string)
    """

    logger.debug(f"Function {get_mask_card_number.__name__} called with parameters: [private data]")
    masked_card_number = ""

    try:
        logger.info("Trying to mask card number")
        masked_card_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        logger.info("Masked successfully")

    except Exception as e:
        logger.error(message_empty_string.format(f"Unable to execute masking, an error occurred: {e}"))

    return masked_card_number


def get_mask_account(account_number: Optional[Any] = None) -> str:
    """
    Masks bank account number for secure display.

    Args:
        account_number: Bank account number as string (20 digits)

    Returns:
         masked_account_number: hidden account number in '**XXXX' format (string)
    """

    logger.debug(f"Function {get_mask_account.__name__} called with parameters: [private data]")
    masked_account_number = ""

    try:
        logger.info("Trying to mask account number")
        masked_account_number = f"**{account_number[-4:]}"
        logger.info("Masked successfully")

    except Exception as e:
        logger.error(message_empty_string.format(f"Unable to execute masking, an error occurred: {e}"))

    return masked_account_number
