"""
Tests for src/widget.py
"""

import pytest

from widget import get_date, mask_account_card

'''
Tests for mask_account_card
'''


def test_mask_account_card_valid(valid_bank_data):
    """Tests for valid bank data inputs"""
    input_data, expected = valid_bank_data
    result = mask_account_card(input_data)
    assert result == expected


def test_mask_account_card_invalid_types(invalid_bank_data_type):
    """Tests for invalid data types"""
    result = mask_account_card(invalid_bank_data_type)
    assert "Invalid input" in result
    assert "Input must be a string" in result


def test_mask_account_card_invalid_formats(invalid_bank_data_format):
    """Tests for invalid string formats"""
    result = mask_account_card(invalid_bank_data_format)
    assert "Invalid" in result


def test_mask_account_card_edge_cases(edge_case_bank_data):
    """Tests for edge cases"""
    input_data, expected = edge_case_bank_data
    result = mask_account_card(input_data)
    assert result == expected


'''
Tests for get_date
'''

# Valid cases (dates in ISO-format)


@pytest.mark.parametrize("iso_date,expected", [
    ("2023-10-05T14:30:00", "05.10.2023"),
    ("2023-01-01T00:00:00", "01.01.2023"),
])
def test_get_date_valid(iso_date, expected):
    """Test valid ISO dates"""
    result = get_date(iso_date)
    assert result == expected


# Invalid cases (wrong type or string format is given)

@pytest.mark.parametrize("invalid_input,expected_error", [
    (123, "Invalid input: date must be a string in ISO-format"),
    (None, "Invalid input: date must be a string in ISO-format"),
    (45.67, "Invalid input: date must be a string in ISO-format"),
    ("not-a-date", "Invalid input: date must be a string in ISO-format"),
    ("2023-13-01T14:30:00", "Invalid input: date must be a string in ISO-format"),
])
def test_get_date_invalid(invalid_input, expected_error):
    """Test invalid inputs"""
    result = get_date(invalid_input)
    assert result == expected_error
    assert "Invalid input" in result
    assert "ISO-format" in result


