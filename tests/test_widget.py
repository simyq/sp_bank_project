"""
Tests for src/widget.py
"""

import pytest

from widget import get_date, mask_account_card

"""
Tests for mask_account_card
"""


def test_mask_account_card_valid(valid_bank_data):
    """Tests for valid bank data inputs"""
    input_data, expected = valid_bank_data
    result = mask_account_card(input_data)
    assert result == expected


def test_mask_account_card_invalid_types(invalid_bank_data_type):
    """Tests for invalid data types"""
    with pytest.raises(ValueError, match="Input must be a string"):
        mask_account_card(invalid_bank_data_type)


def test_mask_account_card_invalid_formats(invalid_bank_data_format):
    """Tests for invalid string formats"""
    with pytest.raises(ValueError) as exc_info:
        mask_account_card(invalid_bank_data_format)

    # Проверяем, что сообщение об ошибке содержит ключевые слова
    error_message = str(exc_info.value)
    assert "Input must be a string" in error_message or "Empty input" in error_message or "16 digits" in error_message or "20 digits" in error_message


def test_mask_account_card_edge_cases(edge_case_bank_data):
    """Tests for edge cases"""
    input_data, expected = edge_case_bank_data
    result = mask_account_card(input_data)
    assert result == expected


"""
Tests for get_date
"""

# Valid cases (dates in ISO-format)
@pytest.mark.parametrize(
    "iso_date,expected",
    [
        ("2023-10-05T14:30:00", "05.10.2023"),
        ("2023-01-01T00:00:00", "01.01.2023"),
        ("2023-10-05", "05.10.2023"),
    ],
)
def test_get_date_valid(iso_date, expected):
    """Test valid ISO dates"""
    result = get_date(iso_date)
    assert result == expected

# Invalid cases (wrong type or string format is given)
@pytest.mark.parametrize(
    "invalid_input",
    [
        123,
        None,
        45.67,
    ],
)
def test_get_date_invalid_types(invalid_input):
    """Test invalid input types"""
    with pytest.raises(TypeError, match="Invalid input: date must be a string in ISO-format"):
        get_date(invalid_input)

@pytest.mark.parametrize(
    "invalid_date_string",
    [
        "not-a-date",
        "2023-13-01T14:30:00",
        "2023-02-30T14:30:00",
        "14:30:00",
        "2023-10-05T25:00:00",
        "2023-10-05T14:60:00",
        "2023-10-05T14:30:70",
        "",
        "2023/10/05",
    ],
)
def test_get_date_invalid_strings(invalid_date_string):
    """Test invalid date strings"""
    with pytest.raises(ValueError):
        get_date(invalid_date_string)
