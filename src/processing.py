"""
Module with functions filter_by_state for filtering lists by state and sort_by_date for sorting lists by date
"""


def filter_by_state(list_with_dicts: list[dict], state: str = "EXECUTED") -> list:
    """
    Sorts list by the parameter state (key 'state' in dictionary)
    :param list_with_dicts: list with dictionaries inside
    :param state: optional parameter to filter list by state (EXECUTED/CANCELED),
        default value is 'EXECUTED' if not given or incorrect value given when function is called
    :return: filtered_list_by_state: items from primary list if they have given state as value in dictionary['state']
    """

    filtered_list_by_state = [item for item in list_with_dicts if item['state'] == state]

    return filtered_list_by_state


def sort_by_date(list_with_dicts: list[dict], descending: bool = True) -> list:
    """
    Sorts list by the parameter date (key 'date' in dictionary)
    :param list_with_dicts: list with dictionaries inside
    :param descending: bool parameter for sorting list by date
        (True is descending order, False is ascending, default is descending)
    :return: sorted_list_by_date: sorted given list by date depending on given order
    """

    sorted_list_by_date = sorted(list_with_dicts, key=lambda item: item['date'], reverse=descending)

    return sorted_list_by_date
