"""
Tests for processing.py
"""

from processing import filter_by_state, sort_by_date

# TESTS FOR filter_by_state


def test_filter_by_state_valid(sample_transactions, valid_filter_state_data):
    """Tests valid state filtering"""
    state, expected_ids = valid_filter_state_data
    result = filter_by_state(sample_transactions, state)
    result_ids = [item['id'] for item in result]
    assert result_ids == expected_ids


def test_filter_by_state_invalid_state(sample_transactions, invalid_filter_state_data):
    """Tests filtering with invalid state values"""
    state = invalid_filter_state_data
    result = filter_by_state(sample_transactions, state)
    assert result == []


def test_filter_by_state_edge_cases(edge_filter_state_data):
    """Tests edge cases for state filtering"""
    data, state = edge_filter_state_data
    result = filter_by_state(data, state)
    assert isinstance(result, list)


def test_filter_by_state_default_behavior(sample_transactions):
    """Tests default parameter behavior"""
    result_default = filter_by_state(sample_transactions)
    result_explicit = filter_by_state(sample_transactions, 'EXECUTED')
    assert result_default == result_explicit


def test_filter_by_state_original_unchanged(sample_transactions):
    """Tests that original list is not modified"""
    original_copy = sample_transactions.copy()
    filter_by_state(sample_transactions, 'EXECUTED')
    assert sample_transactions == original_copy


# TESTS FOR sort_by_date


def test_sort_by_date_valid(sample_transactions, valid_sort_date_data):
    """Tests valid date sorting"""
    descending, expected_first_date = valid_sort_date_data
    result = sort_by_date(sample_transactions, descending)
    assert result[0]['date'] == expected_first_date


def test_sort_by_date_invalid_param(sample_transactions, invalid_sort_date_param):
    """Tests sorting with invalid sorting parameter"""
    result = sort_by_date(sample_transactions, invalid_sort_date_param)
    assert isinstance(result, list)


def test_sort_by_date_edge_cases(edge_sort_date_data):
    """Tests edge cases for date sorting"""
    data = edge_sort_date_data
    result = sort_by_date(data, True)
    assert isinstance(result, list)
    assert len(result) == len(data)


def test_sort_by_date_default_behavior(sample_transactions):
    """Tests default sorting behavior"""
    result_default = sort_by_date(sample_transactions)
    result_explicit = sort_by_date(sample_transactions, True)
    assert result_default == result_explicit
