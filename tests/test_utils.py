"""Tests for module utils.py"""

from unittest.mock import mock_open, patch

import pytest

from utils import read_json_file

#For testing clear function, without decorator
original_read_json_file = read_json_file.__wrapped__

# Valid cases
def test_read_json_file_valid_json_list():
    """Test reading valid JSON file containing a list"""
    json_content = '[{"id": 1, "name": "test"}, {"id": 2, "name": "test2"}]'

    with patch('builtins.open', mock_open(read_data=json_content)):
        result = original_read_json_file("valid.json")

        assert result == [{"id": 1, "name": "test"}, {"id": 2, "name": "test2"}]
        assert isinstance(result, list)
        assert len(result) == 2


def test_read_json_file_empty_json_list():
    """Test reading JSON file containing empty list"""
    json_content = '[]'

    with patch('builtins.open', mock_open(read_data=json_content)):
        result = original_read_json_file("empty_list.json")

        assert result == []
        assert isinstance(result, list)


def test_read_json_file_complex_nested_structure():
    """Test reading JSON with complex nested structure"""
    json_content = '''
    [
        {
            "id": 1,
            "data": {
                "nested": ["a", "b", "c"],
                "numbers": [1, 2, 3]
            },
            "tags": ["tag1", "tag2"]
        }
    ]
    '''

    with patch('builtins.open', mock_open(read_data=json_content)):
        result = original_read_json_file("complex.json")

        assert len(result) == 1
        assert result[0]["id"] == 1
        assert result[0]["data"]["nested"] == ["a", "b", "c"]
        assert result[0]["tags"] == ["tag1", "tag2"]


# Edge cases
def test_read_json_file_json_not_list():
    """Test when JSON is valid but not a list (should return empty list)"""
    # JSON object instead of list
    json_content = '{"id": 1, "name": "test"}'

    with patch('builtins.open', mock_open(read_data=json_content)):
        result = original_read_json_file("not_list.json")

        assert result == []
        assert isinstance(result, list)


def test_read_json_file_single_item_list():
    """Test JSON file with single item in list"""
    json_content = '[{"single": "item"}]'

    with patch('builtins.open', mock_open(read_data=json_content)):
        result = original_read_json_file("single.json")

        assert result == [{"single": "item"}]
        assert len(result) == 1


def test_read_json_file_large_numbers():
    """Test reading JSON with large numbers and floats"""
    json_content = '[{"id": 9999999999, "price": 12345.67, "quantity": 0.001}]'

    with patch('builtins.open', mock_open(read_data=json_content)):
        result = original_read_json_file("numbers.json")

        assert result == [{"id": 9999999999, "price": 12345.67, "quantity": 0.001}]


def test_read_json_file_decorator_file_not_exists():
    """Test that decorator prevents file reading when file doesn't exist"""
    # Mock Path checks to simulate non-existent file
    with patch('pathlib.Path.exists') as mock_exists:
        mock_exists.return_value = False

    with pytest.raises(FileNotFoundError):
        result = original_read_json_file("nonexistent.json")



# Invalid cases
def test_read_json_file_invalid_json_syntax():
    """Test reading file with invalid JSON syntax"""
    invalid_json = '[{"id": 1, "name": test}]'  # Missing quotes around "test"

    with patch('builtins.open', mock_open(read_data=invalid_json)):
        result = original_read_json_file("invalid_syntax.json")

        # Should catch JSONDecodeError and return empty list
        assert result == []


def test_read_json_file_empty_string():
    """Test reading completely empty file (empty string)"""
    with patch('builtins.open', mock_open(read_data='')):
        result = original_read_json_file("empty.json")

        # Should catch JSONDecodeError and return empty list
        assert result == []


def test_read_json_file_whitespace_only():
    """Test reading file with only whitespace"""
    with patch('builtins.open', mock_open(read_data='   \n\t  \n')):
        result = original_read_json_file("whitespace.json")

        # Should catch JSONDecodeError and return empty list
        assert result == []


def test_read_json_file_file_read_error():
    """Test when file reading causes OSError"""
    with patch('builtins.open') as mock_file:
        mock_file.side_effect = OSError("Permission denied")

        with pytest.raises(OSError):
            result = original_read_json_file("protected.json")


def test_read_json_file_unicode_decode_error():
    """Test when file has invalid UTF-8 encoding"""
    with patch('builtins.open') as mock_file:
        # Simulate binary data that can't be decoded as UTF-8
        mock_file.side_effect = UnicodeDecodeError('utf-8', b'\xff', 0, 1, 'invalid start byte')

        with pytest.raises(UnicodeDecodeError):
            result = original_read_json_file("invalid_encoding.json")


def test_read_json_file_null_in_json():
    """Test JSON containing null values"""
    json_content = '[{"id": 1, "value": null}, {"id": 2, "value": "not null"}]'

    with patch('builtins.open', mock_open(read_data=json_content)):
        result = original_read_json_file("with_null.json")

        assert result == [{"id": 1, "value": None}, {"id": 2, "value": "not null"}]

