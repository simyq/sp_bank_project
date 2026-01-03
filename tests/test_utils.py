"""Tests for module utils.py"""

import pytest
import json
from unittest.mock import Mock, patch, mock_open, MagicMock
from pathlib import Path
from utils import read_json_file

# Test data
VALID_JSON_LIST = '[{"id": 1, "name": "test1"}, {"id": 2, "name": "test2"}]'
VALID_JSON_EMPTY_LIST = '[]'
VALID_JSON_COMPLEX = '[{"id": 1, "data": {"nested": "value"}, "list": [1, 2, 3]}]'
INVALID_JSON_NOT_LIST = '{"id": 1, "name": "test"}'
INVALID_JSON_SYNTAX = '[{"id": 1, name: "test"}]'  # missing quotes


# Fixtures
@pytest.fixture
def mock_get_data_path():
    """Mock для get_data_path"""

    def _mock_get_data_path(filename: str) -> Path:
        mock_path = Mock(spec=Path)
        mock_path.exists = Mock()
        mock_path.is_file = Mock()
        mock_path.stat = Mock()
        mock_path.__str__ = Mock(return_value=f"/mock/path/{filename}")
        return mock_path

    return _mock_get_data_path


@pytest.fixture
def mock_logger():
    """Mock для logger"""
    with patch('utils.logger') as mock_logger:
        yield mock_logger


# Valid cases
@patch('utils.get_data_path')
def test_read_json_file_valid_list(mock_get_data_path, mock_logger):
    """Test reading valid JSON file with list"""
    # Setup mock path
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_stat = Mock()
    mock_stat.st_size = 100
    mock_path.stat.return_value = mock_stat
    mock_get_data_path.return_value = mock_path

    # Mock file reading
    with patch('builtins.open', mock_open(read_data=VALID_JSON_LIST)):
        result = read_json_file("valid.json")

        # Verify calls
        mock_get_data_path.assert_called_once_with("valid.json")
        mock_path.exists.assert_called_once()
        mock_path.is_file.assert_called_once()
        mock_path.stat.assert_called_once()

        # Verify result
        assert result == [{"id": 1, "name": "test1"}, {"id": 2, "name": "test2"}]
        assert isinstance(result, list)
        assert len(result) == 2

        # Verify logging
        mock_logger.debug.assert_called()
        mock_logger.info.assert_called()
        mock_logger.error.assert_not_called()
        mock_logger.critical.assert_not_called()


@patch('utils.get_data_path')
def test_read_json_file_complex_structure(mock_get_data_path, mock_logger):
    """Test reading JSON with complex nested structure"""
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_stat = Mock()
    mock_stat.st_size = 100
    mock_path.stat.return_value = mock_stat
    mock_get_data_path.return_value = mock_path

    with patch('builtins.open', mock_open(read_data=VALID_JSON_COMPLEX)):
        result = read_json_file("complex.json")

        assert result == [{"id": 1, "data": {"nested": "value"}, "list": [1, 2, 3]}]
        assert isinstance(result[0]['data'], dict)
        assert isinstance(result[0]['list'], list)


@patch('utils.get_data_path')
def test_read_json_file_empty_list(mock_get_data_path, mock_logger):
    """Test reading JSON file with empty list"""
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_stat = Mock()
    mock_stat.st_size = 100
    mock_path.stat.return_value = mock_stat
    mock_get_data_path.return_value = mock_path

    with patch('builtins.open', mock_open(read_data=VALID_JSON_EMPTY_LIST)):
        result = read_json_file("empty_list.json")

        assert result == []
        assert isinstance(result, list)

        # Should log debug message about data being valid
        mock_logger.debug.assert_called_with("Data is valid")


# Invalid cases
@patch('utils.get_data_path')
def test_read_json_file_invalid_json_syntax(mock_get_data_path, mock_logger):
    """Test when JSON has syntax errors"""
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_stat = Mock()
    mock_stat.st_size = 100
    mock_path.stat.return_value = mock_stat
    mock_get_data_path.return_value = mock_path

    with patch('builtins.open', mock_open(read_data=INVALID_JSON_SYNTAX)):
        result = read_json_file("invalid.json")

        assert result == []
        # Should log critical error
        mock_logger.critical.assert_called()


# Edge cases
def test_read_json_file_none_filename(mock_logger):
    """Test with None filename"""
    result = read_json_file(None)

    assert result == []
    mock_logger.error.assert_called_with(
        "No arguments have been given or given arguments None are invalid. Returning an empty list"
    )


def test_read_json_file_non_string_filename(mock_logger):
    """Test with non-string filename"""
    result = read_json_file(123)

    assert result == []
    mock_logger.error.assert_called_with(
        "No arguments have been given or given arguments 123 are invalid. Returning an empty list"
    )


@patch('utils.get_data_path')
def test_read_json_file_empty_string_filename(mock_get_data_path, mock_logger):
    """Test with empty string filename"""
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = False  # Empty string path doesn't exist
    mock_get_data_path.return_value = mock_path

    result = read_json_file("")

    assert result == []
    mock_logger.error.assert_called_with(
        'JSON-file "" does not exist or is empty. Returning an empty list'
    )


@patch('utils.get_data_path')
def test_read_json_file_file_not_exists(mock_get_data_path, mock_logger):
    """Test when file doesn't exist"""
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = False
    mock_get_data_path.return_value = mock_path

    result = read_json_file("nonexistent.json")

    assert result == []
    mock_path.is_file.assert_not_called()
    mock_path.stat.assert_not_called()
    mock_logger.error.assert_called()


@patch('utils.get_data_path')
def test_read_json_file_path_is_directory(mock_get_data_path, mock_logger):
    """Test when path is a directory, not a file"""
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = False
    mock_get_data_path.return_value = mock_path

    result = read_json_file("directory/")

    assert result == []
    mock_path.stat.assert_not_called()
    mock_logger.error.assert_called()


@patch('utils.get_data_path')
def test_read_json_file_empty_file(mock_get_data_path, mock_logger):
    """Test when file exists but is empty"""
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_stat = Mock()
    mock_stat.st_size = 0  # Empty file
    mock_path.stat.return_value = mock_stat
    mock_get_data_path.return_value = mock_path

    result = read_json_file("empty.json")

    assert result == []
    mock_logger.error.assert_called()


# Parameterized tests
@pytest.mark.parametrize("json_content,expected_result", [
    (VALID_JSON_LIST, [{"id": 1, "name": "test1"}, {"id": 2, "name": "test2"}]),
    (VALID_JSON_EMPTY_LIST, []),
    (VALID_JSON_COMPLEX, [{"id": 1, "data": {"nested": "value"}, "list": [1, 2, 3]}]),
])
@patch('utils.get_data_path')
def test_read_json_file_valid_cases_parameterized(mock_get_data_path, json_content, expected_result, mock_logger):
    """Parameterized test for valid JSON cases"""
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_stat = Mock()
    mock_stat.st_size = 100
    mock_path.stat.return_value = mock_stat
    mock_get_data_path.return_value = mock_path

    with patch('builtins.open', mock_open(read_data=json_content)):
        result = read_json_file("test.json")

        assert result == expected_result


@pytest.mark.parametrize("filename,expected_error_log", [
    (None, "No arguments have been given or given arguments None are invalid"),
    (123, "No arguments have been given or given arguments 123 are invalid"),
    ("", 'JSON-file "" does not exist or is empty'),
])
def test_read_json_file_invalid_parameters(filename, expected_error_log, mock_logger):
    """Parameterized test for invalid parameters"""
    if isinstance(filename, str) and filename == "":
        with patch('utils.get_data_path') as mock_get_data_path:
            mock_path = Mock(spec=Path)
            mock_path.exists.return_value = False
            mock_get_data_path.return_value = mock_path
            result = read_json_file(filename)
    else:
        result = read_json_file(filename)

    assert result == []
    mock_logger.error.assert_called_with(f"{expected_error_log}. Returning an empty list")
