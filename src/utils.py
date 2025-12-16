"""Module for reading, checking, uploading JSON-files"""

import json
from typing import Optional

from decorators import open_file_safely


@open_file_safely
def read_json_file(json_file: Optional[str] = None) -> list:
    """
    Takes info from JSON-file and returns it as a list of dicts
    :param json_file: path to JSON-file
    :return: data: list of dicts, returns an empty list if file is not found, is empty or contains not list-type data
    """

    data = []

    with open(json_file, "r", encoding="utf-8") as file:

        try:
            data = json.load(file)

        except (json.JSONDecodeError, OSError, UnicodeDecodeError):
            return []

    return data if isinstance(data, list) else []
