"""Main module of the program, currently contains only tests for masks.py"""

from masks import get_mask_account, get_mask_card_number


def main() -> None:
    """
    Main function of the program

    Args:
        No arguments (None)

    Returns:
        None
    """

    print(get_mask_card_number(1234567890123456))
    print(get_mask_card_number(123456789012))
    print(get_mask_card_number(None))
    print(get_mask_card_number(True))
    print(get_mask_card_number(123456789.12))

    print(get_mask_account(73654108430135874305))
    print(get_mask_account(1234567890123456))
    print(get_mask_account(123456789012))
    print(get_mask_account(None))
    print(get_mask_account(True))
    print(get_mask_account(123456789))


if __name__ == "__main__":
    main()
