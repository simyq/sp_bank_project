"""Module for opening transactions files (csv and xlsx)"""

import pandas as pd


def read_transactions_csv(file_path: str) -> list[dict]:
    """Takes a path to a csv file and returns a list of dictionaries.
    :param file_path: Path to the csv file
    :return: List of dictionaries"""

    transactions_csv = pd.read_csv(file_path, delimiter=";")
    result = transactions_csv.to_dict("records")

    return result


def read_transactions_excel(file_path: str) -> list[dict]:
    """Takes a path to an excel file and returns a list of dictionaries.
    :param file_path: Path to the excel file
    :return: List of dictionaries"""

    transactions_excel = pd.read_excel(file_path)
    result = transactions_excel.to_dict("records")

    return result
