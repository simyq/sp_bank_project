"""Module for searching and counting operations within json-like bank operations data"""

import re
from collections import Counter


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Takes a list of bank operations data and a search string
    :param data: list of bank operations data
    :param search: search string
    :return: list of bank operations data with given string in their description.
    If nothing found, returns an empty list
    """

    suitable_operations = []

    for operation in data:

        if operation:  # checks if dictionary or list is empty or not
            operation_description = str(
                operation.get("description")
            )  # str() here is used for handling None-type values (if there is no description)
            match = re.search(search, operation_description, flags=re.IGNORECASE)
            if match:
                suitable_operations.append(operation)

    return suitable_operations


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Takes a list of bank operations data and a list of categories to count in operations descriptions
    :param data: list of bank operations data
    :param categories: list of categories to count
    :return: list of bank operations data with given categories"""

    list_of_descriptions = [
        data[n].get("description") for n in range(len(data)) if data[n].get("description") in categories
    ]
    counted_operations = dict(Counter(list_of_descriptions))

    return counted_operations
