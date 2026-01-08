"""Tests for operations.py"""

import pytest

from operations import process_bank_operations, process_bank_search

# Test data
SAMPLE_OPERATIONS = [
    {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {
            "amount": "31957.58",
            "currency": {"name": "руб.", "code": "RUB"}
        },
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589"
    },
    {
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {
            "amount": "8221.37",
            "currency": {"name": "USD", "code": "USD"}
        },
        "description": "Перевод организации",
        "from": "MasterCard 7158300734726758",
        "to": "Счет 35383033474447895560"
    },
    {
        "id": 587085106,
        "state": "EXECUTED",
        "date": "2018-03-23T10:45:06.972075",
        "operationAmount": {
            "amount": "48223.05",
            "currency": {"name": "руб.", "code": "RUB"}
        },
        "description": "Открытие вклада",
        "to": "Счет 41421565395219882431"
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {
            "amount": "56883.54",
            "currency": {"name": "USD", "code": "USD"}
        },
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229"
    },
    {
        "id": 518707726,
        "state": "EXECUTED",
        "date": "2018-11-29T07:18:23.941293",
        "operationAmount": {
            "amount": "3348.98",
            "currency": {"name": "USD", "code": "USD"}
        },
        "description": "Перевод с карты на карту",
        "from": "MasterCard 3152479541115065",
        "to": "Visa Gold 9447344650495960"
    },
    {
        "id": 104807525,
        "state": "EXECUTED",
        "date": "2019-06-01T06:46:16.803326",
        "operationAmount": {
            "amount": "60888.63",
            "currency": {"name": "руб.", "code": "RUB"}
        },
        "description": "Перевод с карты на счет",
        "from": "МИР 8201420097886664",
        "to": "Счет 35116633516390079956"
    },
    {},  # Empty dictionary for edge case testing
]

'''Tests for process_bank_operations'''

# Valid cases
def test_process_bank_search_find_by_description():
    """Test finding operations by description text"""
    result = process_bank_search(SAMPLE_OPERATIONS, "Перевод организации")

    assert len(result) == 2
    assert all(op["description"] == "Перевод организации" for op in result)
    assert result[0]["id"] == 441945886
    assert result[1]["id"] == 41428829


def test_process_bank_search_case_insensitive():
    """Test case-insensitive search"""
    result_lower = process_bank_search(SAMPLE_OPERATIONS, "перевод организации")
    result_upper = process_bank_search(SAMPLE_OPERATIONS, "ПЕРЕВОД ОРГАНИЗАЦИИ")
    result_mixed = process_bank_search(SAMPLE_OPERATIONS, "ПеРеВоД оРгАнИзАцИи")

    # All should return the same results
    assert len(result_lower) == len(result_upper) == len(result_mixed) == 2
    assert result_lower == result_upper == result_mixed


def test_process_bank_search_partial_match():
    """Test partial string matching"""
    result = process_bank_search(SAMPLE_OPERATIONS, "Перевод")

    # Should find all operations with "Перевод" in description
    assert len(result) == 5  # Все операции с "Перевод" в описании
    descriptions = [op["description"] for op in result]
    assert all("Перевод" in desc for desc in descriptions)


# Edge cases
def test_process_bank_search_empty_list():
    """Test with empty operations list"""
    result = process_bank_search([], "Перевод")

    assert result == []
    assert isinstance(result, list)


def test_process_bank_search_no_matches():
    """Test when no operations match the search"""
    result = process_bank_search(SAMPLE_OPERATIONS, "ihsdjafigij")

    assert result == []
    assert isinstance(result, list)


'''Tests for process_bank_operations function'''

# Valid cases
def test_process_bank_operations_single_category():
    """Test counting operations for single category"""
    categories = ["Перевод организации"]
    result = process_bank_operations(SAMPLE_OPERATIONS, categories)

    assert isinstance(result, dict)
    assert len(result) == 1
    assert result["Перевод организации"] == 2


def test_process_bank_operations_multiple_categories():
    """Test counting operations for multiple categories"""
    categories = ["Перевод организации", "Открытие вклада", "Перевод с карты на карту"]
    result = process_bank_operations(SAMPLE_OPERATIONS, categories)

    assert isinstance(result, dict)
    assert len(result) == 3
    assert result["Перевод организации"] == 2
    assert result["Открытие вклада"] == 1
    assert result["Перевод с карты на карту"] == 2


def test_process_bank_operations_all_categories():
    """Test counting all unique categories in data"""
    # Все уникальные описания из SAMPLE_OPERATIONS
    all_categories = [
        "Перевод организации",
        "Открытие вклада",
        "Перевод с карты на карту",
        "Перевод с карты на счет"
    ]

    result = process_bank_operations(SAMPLE_OPERATIONS, all_categories)

    assert isinstance(result, dict)
    assert len(result) == 4
    assert result["Перевод организации"] == 2
    assert result["Открытие вклада"] == 1
    assert result["Перевод с карты на карту"] == 2
    assert result["Перевод с карты на счет"] == 1


# Edge cases
def test_process_bank_operations_empty_data():
    """Test with empty operations list"""
    result = process_bank_operations([], ["Перевод организации"])

    assert result == {}
    assert isinstance(result, dict)


def test_process_bank_operations_empty_categories():
    """Test with empty categories list"""
    result = process_bank_operations(SAMPLE_OPERATIONS, [])

    assert result == {}
    assert isinstance(result, dict)


def test_process_bank_operations_no_matching_categories():
    """Test when no operations match any category"""
    categories = ["Нет такой категории", "Другая категория"]
    result = process_bank_operations(SAMPLE_OPERATIONS, categories)

    assert result == {}
    assert isinstance(result, dict)


def test_process_bank_operations_skips_empty_dicts():
    """Test that function skips empty dictionaries"""
    operations_with_empty = [
        {},
        {"id": 1, "description": "Категория A"},
        {},
        {"id": 2, "description": "Категория A"},
        {"id": 3, "description": "Категория B"},
        {}
    ]

    categories = ["Категория A", "Категория B"]
    result = process_bank_operations(operations_with_empty, categories)

    assert result == {"Категория A": 2, "Категория B": 1}


def test_process_bank_operations_case_sensitive():  # Case-insensitiveness is applied directly to the user's input
    """Test that function is case-sensitive (exact match required)"""
    operations = [
        {"id": 1, "description": "Перевод"},
        {"id": 2, "description": "перевод"},  # lowercase
        {"id": 3, "description": "ПЕРЕВОД"}  # uppercase
    ]

    # Should only match exact case
    result = process_bank_operations(operations, ["Перевод"])

    assert result == {"Перевод": 1}  # Only the first one matches


def test_process_bank_operations_duplicate_categories():
    """Test with duplicate categories in input list"""
    categories = ["Перевод организации", "Перевод организации", "Открытие вклада"]
    result = process_bank_operations(SAMPLE_OPERATIONS, categories)

    # Duplicates in categories should not affect counting
    assert result == {"Перевод организации": 2, "Открытие вклада": 1}


# Invalid cases
def test_process_bank_operations_none_data():
    """Test with None instead of data list"""

    with pytest.raises(TypeError):
        process_bank_operations(None, ["Перевод организации"])


def test_process_bank_operations_none_categories():
    """Test with None instead of categories list"""

    with pytest.raises(TypeError):
        process_bank_operations(SAMPLE_OPERATIONS, None)


def test_process_bank_operations_missing_description_key():
    """Test when some operations don't have description key"""
    operations_missing_desc = [
        {"id": 1, "description": "Категория A"},
        {"id": 2},  # Missing description
        {"id": 3, "description": "Категория A"},
        {"id": 4, "description": "Категория B"}
    ]

    categories = ["Категория A", "Категория B"]
    result = process_bank_operations(operations_missing_desc, categories)

    # Should skip operations without description
    assert result == {"Категория A": 2, "Категория B": 1}


def test_process_bank_operations_non_string_description():
    """Test when description is not a string"""
    operations_non_string_desc = [
        {"id": 1, "description": "Категория A"},
        {"id": 2, "description": 123},  # Integer instead of string
        {"id": 3, "description": None},  # None instead of string
        {"id": 4, "description": "Категория A"}
    ]

    categories = ["Категория A", "Категория B"]
    result = process_bank_operations(operations_non_string_desc, categories)

    # Should handle non-string descriptions gracefully
    # Only string descriptions that match categories should be counted
    assert result == {"Категория A": 2}
