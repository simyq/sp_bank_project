"""
Module with generator functions. Helps to work with arrays (collections) of transactions by sorting.
Also contains generator for creating card number
(Might be upgraded for creating Visa, Maestro and other types of cards with locked first numbers)
(Also might be updated by list (or file) with cards, that already exist)
Unused function in comments at the end of the module
might be used to work with string format input for card number generating
"""

from typing import Any, Generator


def filter_by_currency(transactions: list[dict], currency: str) -> filter:
    """
    Generator function. Filters transactions by currency.
    :param transactions: list with dictionaries (info about transactions)
    :param currency: string of currency (ex. 'USD', 'EUR', 'BYR', 'RUB')
    :return: filter object with filtered transactions
    """

    filtered_transactions = filter(
        lambda trans: trans["operationAmount"]["currency"]["code"] == currency.upper(), transactions
    )

    return filtered_transactions


def get_transaction_descriptions(transactions: list[dict]) -> Generator:
    """
    Function for getting descriptions of given transactions
    :param transactions: list with dictionaries (info about transactions)
    :return: Generator object: Generator with transactions descriptions
    """

    description_generator =  (transaction["description"] for transaction in transactions)
    yield from description_generator


def card_number_generator(start: Any, stop: Any) -> Generator[str, Any, None]:
    """
    Generator function for generating card numbers inside of given range.
    :param start: takes any type of parameter, but must be an integer (starting number for creating a card number).
    :param stop: takes any type of parameter, but must be an integer (ending number for creating a card number).
    Both start and stop must be integers in format from 1 to 9999999999999999
    :return: Generator: Generator with generated card numbers in format 'XXXX XXXX XXXX XXXX'.
    If validation fails on any step, raises an error.
    """

    try:
        if not start or not stop:
            raise ValueError("Not all arguments have been given or '0' given as an argument")

        if not isinstance(start, int) or not isinstance(stop, int):
            raise TypeError("Arguments must be integers")

        if start > stop or start < 1 or stop > 9999999999999999:
            raise ValueError(
                "Arguments must be between 1 and 9999999999999999. Start must be less than or equal to stop"
            )

        for i in range(start, stop + 1):
            card_num = str(i).zfill(16)
            formatted_card = f"{card_num[:4]} {card_num[4:8]} {card_num[8:12]} {card_num[12:16]}"
            yield formatted_card

    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid input: {e}") from e


'''
def card_number_generator(start: Any, stop: Any) -> Generator[str, Any, None]:
    """
    Generator function for generating card numbers inside of given range.
    :param start: takes any type of parameter, but must be a string with starting number for creating a card number.
    :param stop: takes any type of parameter, but must be a string with ending number for creating a card number.
    Both start and stop must be strings in format 'XXXXXXXXXXXXXXXX', where 'X' is digit,
    whole number must be in range from 0000000000000001 to 9999999999999999.
    :return: Generator: Generator with generated card numbers in format 'XXXX XXXX XXXX XXXX'.
    If validation fails on any step, raises an error.
    """
    try:
        if not isinstance(start, str) or not isinstance(stop, str):
            raise TypeError("Arguments must be strings")

        mod_start = start.strip()
        mod_stop = stop.strip()

        if len(mod_start) != 16 or len(mod_stop) != 16 or not mod_start.isdigit() or not mod_stop.isdigit():
            raise ValueError("Arguments must be 16-digit numbers in string format")

        mod_start = int(mod_start)
        mod_stop = int(mod_stop)

        if mod_start > mod_stop or mod_start < 1:
            raise ValueError("""Arguments must be between 0000000000000001 and 9999999999999999
                             Start must be less than stop""")

        for i in range(mod_start, mod_stop + 1):
            card_num = str(i).zfill(16)
            formatted_card = f"{card_num[:4]} {card_num[4:8]} {card_num[8:12]} {card_num[12:16]}"
            yield formatted_card

    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid input: {e}") from e
'''
