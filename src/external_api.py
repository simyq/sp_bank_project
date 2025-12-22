"""Module for transaction converting, working with API"""

import os
from typing import Any

import requests
from dotenv import load_dotenv


def convert_to_rubles(transaction: dict) -> Any:
    """
    Takes a transaction, finds transaction's amount from json and converts it to RUB
    :param transaction: JSON-formatted transaction from file
    :return: amount: float number — the amount of transaction converted to RUB
    """

    load_dotenv()
    api_key = os.getenv("API_KEY")
    url = "https://api.apilayer.com/exchangerates_data/convert"

    try:

        amount = float(transaction["operationAmount"]["amount"])
        currency = transaction["operationAmount"]["currency"]["code"]
        headers = {"apikey": api_key}
        payload = {"amount": amount, "from": currency, "to": "RUB"}

        if not currency == "RUB":
            response = requests.get(url, headers=headers, params=payload)
            result = response.json()

            return result["result"]

        else:
            return amount

    except Exception as e:
        return f"Something went wrong: {e}"
