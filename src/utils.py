"""Module for reading, checking, uploading JSON-files"""

import json
import logging
from typing import Optional

from config import get_data_path, get_log_path

logger = logging.getLogger("utils_logger")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(filename=get_log_path("utils.log"), mode="w", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s: %(filename)s: %(levelname)s: %(message)s", datefmt="%d-%m-%Y %I:%M:%S")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

message_empty_list = "{}. Returning an empty list"


def read_json_file(json_file: Optional[str] = None) -> list:
    """
    Takes info from JSON-file and returns it as a list of dicts.
    Checks if path to file and file are valid to read
    (if path is not given, if file is not found, is broken (or is not file), or is empty).
    :param json_file: path to JSON-file
    :return: data: list of dicts, returns an empty list if file is not found, is empty or contains not list-type data
    """

    logger.debug(f"Function {read_json_file.__name__} called with parameters: {json_file}")
    data = []

    if isinstance(json_file, str):
        path_to_json_file = get_data_path(json_file)
        logger.info(f"Checking file: {path_to_json_file}")

        if path_to_json_file.exists() and path_to_json_file.is_file() and path_to_json_file.stat().st_size > 0:
            logger.info(f"{path_to_json_file} is valid to read")

            with open(path_to_json_file, "r", encoding="utf-8") as file:

                try:
                    data = json.load(file)

                    if isinstance(data, list):
                        logger.debug("Data is valid")

                    else:
                        logger.debug(message_empty_list.format("Data is invalid"))

                except Exception as e:
                    logger.critical(
                        message_empty_list.format(f'An error occurred while reading file: "{path_to_json_file}". {e}')
                    )

                finally:
                    logger.info(f", returning {len(data)} records")
                    return data
        else:
            logger.error(message_empty_list.format(f'JSON-file "{json_file}" does not exist or is empty'))
            return data

    else:
        logger.error(
            message_empty_list.format(f"No arguments have been given or given arguments {json_file} are invalid")
        )
        return data
