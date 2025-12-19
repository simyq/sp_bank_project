"""Tests for external_api"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import os

from external_api import convert_to_rubles

# Test data
RUB_TRANSACTION = {
    "operationAmount": {
        "amount": "1000.50",
        "currency": {
            "code": "RUB"
        }
    }
}

USD_TRANSACTION = {
    "operationAmount": {
        "amount": "100.00",
        "currency": {
            "code": "USD"
        }
    }
}

EUR_TRANSACTION = {
    "operationAmount": {
        "amount": "50.75",
        "currency": {
            "code": "EUR"
        }
    }
}

INVALID_TRANSACTION_MISSING_AMOUNT = {
    "operationAmount": {
        "currency": {
            "code": "USD"
        }
    }
}

INVALID_TRANSACTION_MISSING_CURRENCY = {
    "operationAmount": {
        "amount": "100.00"
    }
}

INVALID_TRANSACTION_WRONG_TYPE = {
    "operationAmount": {
        "amount": "not_a_number",
        "currency": {
            "code": "USD"
        }
    }
}


# Valid cases
@patch('requests.get')
@patch.dict(os.environ, {'API_KEY': 'test-api-key-123'})
def test_convert_to_rubles_rub_currency(mock_requests_get):
    """Test conversion when currency is already RUB"""
    result = convert_to_rubles(RUB_TRANSACTION)

    # Should return amount directly without API call
    mock_requests_get.assert_not_called()
    assert result == 1000.50
    assert isinstance(result, float)


@patch('requests.get')
@patch.dict(os.environ, {'API_KEY': 'test-api-key-123'})
def test_convert_to_rubles_usd_currency(mock_requests_get):
    """Test conversion from USD to RUB"""
    # Mock successful API response
    mock_response = Mock()
    mock_response.json.return_value = {"result": 7500.00, "success": True}
    mock_requests_get.return_value = mock_response

    result = convert_to_rubles(USD_TRANSACTION)

    # Verify API call
    mock_requests_get.assert_called_once()
    call_args = mock_requests_get.call_args

    # Check headers and params
    assert call_args[1]['headers'] == {"apikey": "test-api-key-123"}
    assert call_args[1]['params'] == {"amount": 100.00, "from": "USD", "to": "RUB"}

    assert result == 7500.00
    assert isinstance(result, float)


@patch('requests.get')
@patch.dict(os.environ, {'API_KEY': 'test-api-key-123'})
def test_convert_to_rubles_eur_currency(mock_requests_get):
    """Test conversion from EUR to RUB"""
    mock_response = Mock()
    mock_response.json.return_value = {"result": 4500.25, "success": True}
    mock_requests_get.return_value = mock_response

    result = convert_to_rubles(EUR_TRANSACTION)

    mock_requests_get.assert_called_once()
    assert result == 4500.25


@patch('requests.get')
@patch.dict(os.environ, {'API_KEY': 'test-api-key-123'})
def test_convert_to_rubles_with_decimal_amount(mock_requests_get):
    """Test conversion with decimal amount"""
    transaction = {
        "operationAmount": {
            "amount": "123.456",
            "currency": {
                "code": "USD"
            }
        }
    }

    mock_response = Mock()
    mock_response.json.return_value = {"result": 9259.20, "success": True}  # 123.456 * 75
    mock_requests_get.return_value = mock_response

    result = convert_to_rubles(transaction)

    assert mock_requests_get.call_args[1]['params']['amount'] == 123.456
    assert result == 9259.20


@patch('requests.get')
@patch.dict(os.environ, {'API_KEY': 'test-api-key-123'})
def test_convert_to_rubles_integer_amount(mock_requests_get):
    """Test conversion with integer amount as string"""
    transaction = {
        "operationAmount": {
            "amount": "500",
            "currency": {
                "code": "USD"
            }
        }
    }

    mock_response = Mock()
    mock_response.json.return_value = {"result": 37500.00, "success": True}
    mock_requests_get.return_value = mock_response

    result = convert_to_rubles(transaction)

    assert mock_requests_get.call_args[1]['params']['amount'] == 500.0
    assert result == 37500.00


# Edge cases
@patch('requests.get')
@patch.dict(os.environ, {'API_KEY': 'test-api-key-123'})
def test_convert_to_rubles_zero_amount(mock_requests_get):
    """Test conversion with zero amount"""
    transaction = {
        "operationAmount": {
            "amount": "0",
            "currency": {
                "code": "USD"
            }
        }
    }

    mock_response = Mock()
    mock_response.json.return_value = {"result": 0.0, "success": True}
    mock_requests_get.return_value = mock_response

    result = convert_to_rubles(transaction)

    assert result == 0.0


@patch('requests.get')
@patch.dict(os.environ, {'API_KEY': 'test-api-key-123'})
def test_convert_to_rubles_negative_amount(mock_requests_get):
    """Test conversion with negative amount"""
    transaction = {
        "operationAmount": {
            "amount": "-100.50",
            "currency": {
                "code": "USD"
            }
        }
    }

    mock_response = Mock()
    mock_response.json.return_value = {"result": -7537.50, "success": True}
    mock_requests_get.return_value = mock_response

    result = convert_to_rubles(transaction)

    assert mock_requests_get.call_args[1]['params']['amount'] == -100.50
    assert result == -7537.50


@patch('requests.get')
@patch.dict(os.environ, {'API_KEY': ''})  # Empty API key
def test_convert_to_rubles_empty_api_key(mock_requests_get):
    """Test with empty API key in environment"""
    mock_response = Mock()
    mock_response.json.return_value = {"result": 7500.00, "success": True}
    mock_requests_get.return_value = mock_response

    result = convert_to_rubles(USD_TRANSACTION)

    # Should still call API with empty key
    assert mock_requests_get.call_args[1]['headers']['apikey'] == ''
    assert result == 7500.00


# Invalid cases
def test_convert_to_rubles_missing_amount():
    """Test when transaction is missing amount"""
    result = convert_to_rubles(INVALID_TRANSACTION_MISSING_AMOUNT)

    assert "Something went wrong" in result
    assert "KeyError" in result or "'amount'" in result


def test_convert_to_rubles_missing_currency():
    """Test when transaction is missing currency code"""
    result = convert_to_rubles(INVALID_TRANSACTION_MISSING_CURRENCY)

    assert "Something went wrong" in result


def test_convert_to_rubles_invalid_amount_type():
    """Test when amount is not a valid number"""
    result = convert_to_rubles(INVALID_TRANSACTION_WRONG_TYPE)

    assert "Something went wrong" in result
    assert "ValueError" in result or "could not convert" in result


@patch('requests.get')
@patch.dict(os.environ, {'API_KEY': 'test-api-key-123'})
def test_convert_to_rubles_api_response_invalid_json(mock_requests_get):
    """Test when API returns invalid JSON response"""
    mock_response = Mock()
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mock_requests_get.return_value = mock_response

    result = convert_to_rubles(USD_TRANSACTION)

    assert "Something went wrong" in result
    assert "ValueError" in result or "Invalid JSON" in result


@patch('requests.get')
@patch.dict(os.environ, {'API_KEY': 'test-api-key-123'})
def test_convert_to_rubles_api_response_missing_result(mock_requests_get):
    """Test when API response doesn't contain 'result' field"""
    mock_response = Mock()
    mock_response.json.return_value = {"success": False, "error": "Invalid currency"}
    mock_requests_get.return_value = mock_response

    result = convert_to_rubles(USD_TRANSACTION)

    assert "Something went wrong" in result
    assert "KeyError" in result or "'result'" in result


def test_convert_to_rubles_none_transaction():
    """Test when transaction is None"""
    result = convert_to_rubles(None)

    assert "Something went wrong" in result
    assert "TypeError" in result or "'NoneType'" in result


def test_convert_to_rubles_empty_transaction():
    """Test when transaction is empty dict"""
    result = convert_to_rubles({})

    assert "Something went wrong" in result
    assert "KeyError" in result or "'operationAmount'" in result


# Test with different currency codes case sensitivity
@patch('requests.get')
@patch.dict(os.environ, {'API_KEY': 'test-api-key-123'})
def test_convert_to_rubles_lowercase_currency(mock_requests_get):
    """Test with lowercase currency code"""
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "usd"  # lowercase
            }
        }
    }

    mock_response = Mock()
    mock_response.json.return_value = {"result": 7500.00, "success": True}
    mock_requests_get.return_value = mock_response

    result = convert_to_rubles(transaction)

    # API should be called with uppercase currency code
    assert mock_requests_get.call_args[1]['params']['from'] == "usd"
    assert result == 7500.00
