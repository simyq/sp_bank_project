"""
Tests for masks.py
"""

import pytest

from masks import get_mask_account, get_mask_card_number

# Valid cases tests (16-digit string for get_mask_card and 20-digit string for get_mask_account)


def test_get_mask_card_number_valid(valid_card_data):
    """Tests for valid card numbers"""
    card_number, expected = valid_card_data
    result = get_mask_card_number(card_number)
    assert result == expected


def test_get_mask_account_valid(valid_account_data):
    """Tests for valid account numbers"""
    account_number, expected = valid_account_data
    result = get_mask_account(account_number)
    assert result == expected


# Invalid data type given as an argument (raise Exception)


def test_get_mask_card_number_invalid(invalid_data_type):
    """Tests for invalid data type given as an argument"""
    assert get_mask_card_number(invalid_data_type) is ''


def test_get_mask_account_invalid(invalid_data_type):
    """Tests for invalid data type given as an argument"""
    assert get_mask_card_number(invalid_data_type) is ''


# Edge and problematic cases (short or long strings, list or tuple type given)
# No Exception raising, but invalid outcome occur


def test_get_mask_card_number_problematic_cases(problematic_card_data):
    """Tests cases when function runs, but returns incorrect data"""
    card_number, expected = problematic_card_data
    result = get_mask_card_number(card_number)
    assert result == expected


def test_get_mask_account_problematic_cases(problematic_account_data):
    """Tests cases when function runs, but returns incorrect data"""
    account_number, expected = problematic_account_data
    result = get_mask_account(account_number)
    assert result == expected
