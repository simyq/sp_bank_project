"""Main module of the program, currently contains only tests for all the modules"""

from src.masks import get_mask_account, get_mask_card_number
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


if __name__ == "__main__":
    main()
