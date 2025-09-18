"""Main module of the program, currently contains only tests for all the modules"""

from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card


def main() -> None:
    """
    Main function of the program

    Args:
        No arguments (None)

    Returns:
        None
    """

    print(get_mask_card_number("1234567890123456"))
    print(get_mask_card_number("123456789012"))
    print(get_mask_card_number("123456789.12"))

    print(get_mask_account("73654108430135874305"))
    print(get_mask_account("1234567890123456"))
    print(get_mask_account("123456789012"))
    print(get_mask_account("123456789"))

    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Maestro 1596837868705199"))
    print(mask_account_card("MasterCard 7158300734726758"))
    print(mask_account_card("Visa Classic 6831982476737658"))
    print(mask_account_card("Visa Platinum 8990922113665229"))
    print(mask_account_card("Visa Gold 5999414228426353"))

    print(mask_account_card("Visa Gold 5999414228426.53"))

    print(mask_account_card("Счет 64686473678894779589"))
    print(mask_account_card("Счет 73654108430135874305"))
    print(mask_account_card("Счет 7365410843013587123"))
    print(mask_account_card("Счет 35383033474447895560"))

    print(mask_account_card("Счёт 35383033474447895560"))
    print(mask_account_card("Счет 35383033474447895.60"))

    print(mask_account_card(None))
    print(mask_account_card(False))
    print(mask_account_card(1546645456654))

    print(get_date("2024-03-11T02:26:18.671407"))
    print(get_date("20203-11T02:26:18.671407"))
    print(get_date("dsdfghjk"))

    print(filter_by_state([{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                           {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                           {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                           {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]))

    print(filter_by_state([{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                           {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                           {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                           {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}], 'CANCELED'))

    print(sort_by_date([{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}], False))

    print(sort_by_date([{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]))


if __name__ == "__main__":
    main()
