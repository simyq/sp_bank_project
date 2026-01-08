"""Main module of the program, uses console to interact with user.
Currently works with data/ directory and files inside of it,
but may be upgraded by adding any file from the place user wants to
"""

import sys
from typing import Callable, Union

from config import get_data_path
from generators import filter_by_currency
from operations import process_bank_search
from processing import filter_by_state, sort_by_date
from table_readers import read_transactions_csv, read_transactions_excel
from utils import read_json_file
from widget import get_date, mask_account_card

GREETING_MESSAGE = """Здравствуйте! Добро пожаловать в программу работы с банковскими транзакциями.
Выберите необходимый пункт меню

(Для выхода из программы в любое время напишите 'quit')
"""

FILE_CHOICE_MESSAGE = """1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла

Введите номер интересующего Вас пункта меню (1-3)"""

INVALID_INPUT_MESSAGE = "Ваш ввод некорректен, повторите попытку"

QUIT_MESSAGE = "Программа завершила работу"


FILTER_MESSAGE = '''Введите статус, по которому необходимо выполнить фильтрацию.
Доступные для фильтровки статусы: "EXECUTED", "CANCELED", "PENDING"'''


SORTING_BY_DATE_MESSAGE = '''Отсортировать операции по дате?
Напишите "да" или "нет"'''

SORTING_ASCENDING_OR_DESCENDING_MESSAGE = '''Отсортировать по возрастанию или по убыванию?
Напишите "по убыванию" или "по возрастанию"'''

FILTER_ONLY_RUB_CURRENCY_MESSAGE = '''Выводить только рублевые транзакции?
Напишите "да" или "нет"'''

FILTER_BY_WORD_CHOICE_MESSAGE = '''Отфильтровать список транзакций по определенному слову в описании?
Напишите "да" или "нет"'''

WORD_TO_FILTER_BY_MESSAGE = "Введите слово для фильтрации"

PROGRAM_EXECUTING_MESSAGE = "Распечатываю итоговый список транзакций..."

FILTER_METHODS_EXECUTION_MESSAGE = """Файл для обработки: {}
Статус фильтрации: {}
Сортировка по дате: {}
Вывод только рублёвых транзакций: {}
Слово для фильтрации: {}
"""
SUCCESS_EXECUTION_MESSAGE = "Всего операций в выборке: {}"

EMPTY_RESULT_EXECUTION_MESSAGE = "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации"

SEPARATOR_BIG = "=" * 80

SEPARATOR_SMALL = "-" * 80


QUIT_CHOICE = "quit"

FILE_CHOICE = {"1": "operations.json", "2": "transactions.csv", "3": "transactions_excel.xlsx"}

FILTER_STATUS_CHOICE = {"executed": "EXECUTED", "canceled": "CANCELED", "pending": "PENDING"}

YES_OR_NO_CHOICE = {"да": True, "нет": False}

ASCENDING_OR_DESCENDING_CHOICE = {"по возрастанию": False, "по убыванию": True}


def quit_program() -> None:
    """Simple function to finish running program (interpreter) at any time"""
    sys.exit(0)


def get_and_formate_user_input() -> str:
    """Function for getting and formating user's input
    :param: None
    :return: formatted_user_input, string with no spaces in lowercase"""

    formatted_user_input = input().strip().lower()

    return formatted_user_input


def compare_user_input(interaction_to_compare: dict) -> Union[str, Callable, None]:
    """Function to compare user input with available interactions
    :param: interaction_to_compare, dict with user input
    :return: None (if user wants to quit), string object from dictionary to get interaction from or recursive function
    """

    user_input = get_and_formate_user_input()

    if user_input == QUIT_CHOICE:
        print(QUIT_MESSAGE)
        quit_program()
        return None
    elif user_input in interaction_to_compare:
        return interaction_to_compare.get(user_input)
    else:
        print(INVALID_INPUT_MESSAGE)
        return compare_user_input(interaction_to_compare)


def choose_file_to_read_from_data_dir(chosen_file: str) -> Union[list, None]:
    """Function for choosing file to read from project/data/
    :param: chosen extension (.xslx/.json/.csv)
    :return: string with chosen path to file from project/data/
    """

    if str(chosen_file).endswith(".json"):
        chosen_file_to_read = read_json_file(chosen_file)

    elif str(chosen_file).endswith(".csv"):
        chosen_file_from_dir = get_data_path(chosen_file)
        chosen_file_to_read = read_transactions_csv(str(chosen_file_from_dir))

    elif str(chosen_file).endswith(".xlsx"):
        chosen_file_from_dir = get_data_path(chosen_file)
        chosen_file_to_read = read_transactions_excel(str(chosen_file_from_dir))

    else:
        return []

    return chosen_file_to_read


def formate_transaction(transaction: dict) -> str:
    """
    Function for forming transaction description
    :param transaction:
    :return:
    """
    transaction_date = transaction.get("date")
    transaction_type = transaction.get("description")
    transaction_from = transaction.get("from")
    transaction_to = transaction.get("to")

    transaction_operation_amount = transaction.get("operationAmount")

    if transaction_operation_amount:
        transaction_amount = transaction_operation_amount.get("amount")
        transaction_currency = transaction_operation_amount.get("currency").get("code")
    else:
        transaction_amount = transaction.get("amount")
        transaction_currency = transaction.get("currency_code")

    if transaction_from and isinstance(transaction_from, str):
        transaction_from_to = mask_account_card(transaction_from) + " -> " + mask_account_card(transaction_to)
    else:
        transaction_from_to = mask_account_card(transaction_to)

    formatted_transaction = f"""
    {get_date(transaction_date)} {transaction_type}
    {transaction_from_to}
    Валюта: {transaction_currency}
    Сумма: {transaction_amount}
    """
    return formatted_transaction


def main() -> None:
    """
    Main function of the program

    Args:
        No arguments (None)

    Returns:
        None
    """

    print(GREETING_MESSAGE)
    print(FILE_CHOICE_MESSAGE)

    user_file_to_read = compare_user_input(FILE_CHOICE)
    chosen_file_from_data_dir = choose_file_to_read_from_data_dir(user_file_to_read)

    print(SEPARATOR_SMALL)

    print(FILTER_MESSAGE)

    chosen_filter_status = compare_user_input(FILTER_STATUS_CHOICE)

    print(SEPARATOR_SMALL)

    print(SORTING_BY_DATE_MESSAGE)

    chosen_date_sorting = compare_user_input(YES_OR_NO_CHOICE)

    print(SEPARATOR_SMALL)

    if chosen_date_sorting:
        print(SORTING_ASCENDING_OR_DESCENDING_MESSAGE)
        chosen_order_sorting = compare_user_input(ASCENDING_OR_DESCENDING_CHOICE)
        print(SEPARATOR_SMALL)
    else:
        chosen_order_sorting = "нет"

    print(FILTER_ONLY_RUB_CURRENCY_MESSAGE)

    chosen_currency_filtrating_rub = compare_user_input(YES_OR_NO_CHOICE)

    print(SEPARATOR_SMALL)

    print(FILTER_BY_WORD_CHOICE_MESSAGE)

    chosen_word_flag_filtrating = compare_user_input(YES_OR_NO_CHOICE)

    # All the sorting and filtering algos

    result = filter_by_state(chosen_file_from_data_dir, chosen_filter_status)

    if chosen_date_sorting:
        result = sort_by_date(result, chosen_order_sorting)
        # This condition won't work if the answer on the question about date filtrating is "no"

    if chosen_currency_filtrating_rub:
        currency = "RUB"
        if user_file_to_read.endswith(".xlsx") or user_file_to_read.endswith(".csv"):
            result = list(filter(lambda trans: trans.get("currency_code") == currency.upper(), result))
            # mock filtering function as there are different formats in different type of files
            # filter_by_currency() works properly on;y with JSON-files
        else:
            result = list(filter_by_currency(result, currency))

    if chosen_word_flag_filtrating:
        print(SEPARATOR_SMALL)
        print(WORD_TO_FILTER_BY_MESSAGE)
        chosen_filter_word = get_and_formate_user_input()
        if chosen_filter_word == QUIT_CHOICE:
            print(QUIT_MESSAGE)
            quit_program()
            return None
        else:
            result = process_bank_search(result, chosen_filter_word)
    else:
        chosen_filter_word = "<слово не указано>"

    print(SEPARATOR_BIG)
    print(
        FILTER_METHODS_EXECUTION_MESSAGE.format(
            user_file_to_read,
            chosen_filter_status,
            "да" if chosen_date_sorting else "нет",
            "да" if chosen_currency_filtrating_rub else "нет",
            chosen_filter_word,
        )
    )
    print(SEPARATOR_BIG)
    print(PROGRAM_EXECUTING_MESSAGE)

    if result:
        print(SUCCESS_EXECUTION_MESSAGE.format(len(result)))
        for transaction in result:
            formatted_transaction = formate_transaction(transaction)
            print(formatted_transaction)

    else:
        print(EMPTY_RESULT_EXECUTION_MESSAGE)

    print(QUIT_MESSAGE)

    return None


if __name__ == "__main__":
    main()
