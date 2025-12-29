"""Tests for module utils.py"""


from pathlib import Path
from unittest.mock import Mock, mock_open, patch

from src.utils import read_json_file

# Mock for PATHS["data"]
mock_data_path = Mock(spec=Path)
mock_data_path.mkdir = Mock()
mock_data_path.__truediv__ = Mock(return_value=Path("/mock/data/path/test.json"))


# Mock for get_data_path
def mock_get_data_path(filename: str) -> Path:
    """Mock для get_data_path"""
    mock_path = Mock()
    mock_path.exists = Mock()
    mock_path.is_file = Mock()
    mock_path.stat = Mock()
    return mock_path


# Valid cases


# Edge cases
@patch('utils.get_data_path', side_effect=mock_get_data_path)
def test_read_json_file_json_not_list(mock_get_data_path):
    """Test when JSON is valid but not a list (should return empty list)"""
    json_content = '{"id": 1, "name": "test"}'

    mock_path = mock_get_data_path("not_list.json")
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.return_value = Mock(st_size=100)

    with patch('builtins.open', mock_open(read_data=json_content)):
        result = read_json_file("not_list.json")

        assert result == []
        assert isinstance(result, list)


@patch('utils.get_data_path', side_effect=mock_get_data_path)
def test_read_json_file_file_not_exists(mock_get_data_path):
    """Test when file does not exist"""
    mock_path = mock_get_data_path("nonexistent.json")
    mock_path.exists.return_value = False

    result = read_json_file("nonexistent.json")

    mock_get_data_path.assert_called_once_with("nonexistent.json")
    mock_path.is_file.assert_not_called()  # is_file() is not called
    mock_path.stat.assert_not_called()

    assert result == []


@patch('utils.get_data_path', side_effect=mock_get_data_path)
def test_read_json_file_path_is_directory(mock_get_data_path):
    """Test when path is a directory, not a file"""
    mock_path = mock_get_data_path("directory/")
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = False

    result = read_json_file("directory/")

    mock_path.stat.assert_not_called()  # stat() is not called if is not file

    assert result == []


@patch('utils.get_data_path', side_effect=mock_get_data_path)
def test_read_json_file_empty_file(mock_get_data_path):
    """Test when file exists but is empty (size = 0)"""
    mock_path = mock_get_data_path("empty.txt")
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.return_value = Mock(st_size=0)

    result = read_json_file("empty.txt")

    assert result == []


def test_read_json_file_none_filename():
    """Test with None filename"""
    result = read_json_file(None)
    assert result == []


def test_read_json_file_non_string_filename():
    """Test with non-string filename (e.g., integer)"""
    result = read_json_file(123)
    assert result == []


# Invalid cases
@patch('utils.get_data_path', side_effect=mock_get_data_path)
def test_read_json_file_invalid_json_syntax(mock_get_data_path):
    """Test reading file with invalid JSON syntax"""
    invalid_json = '[{"id": 1, "name": test}]'  # Missing quotes around "test"

    mock_path = mock_get_data_path("invalid_syntax.json")
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.return_value = Mock(st_size=100)

    with patch('builtins.open', mock_open(read_data=invalid_json)):
        result = read_json_file("invalid_syntax.json")

        assert result == []


@patch('utils.get_data_path', side_effect=mock_get_data_path)
def test_read_json_file_empty_string_file(mock_get_data_path):
    """Test reading completely empty file (empty string)"""
    mock_path = mock_get_data_path("empty.json")
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.return_value = Mock(st_size=100)

    with patch('builtins.open', mock_open(read_data='')):
        result = read_json_file("empty.json")

        assert result == []


@patch('utils.get_data_path', side_effect=mock_get_data_path)
def test_read_json_file_io_error_reading(mock_get_data_path):
    """Test when file reading causes IOError"""
    mock_path = mock_get_data_path("protected.json")
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.return_value = Mock(st_size=100)

    with patch('builtins.open') as mock_open_file:
        mock_open_file.side_effect = IOError("Permission denied")

        result = read_json_file("protected.json")

        assert result == []


@patch('utils.get_data_path', side_effect=mock_get_data_path)
def test_read_json_file_stat_exception(mock_get_data_path):
    """Test when stat() raises an exception"""
    mock_path = mock_get_data_path("protected.txt")
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.side_effect = OSError("Permission denied")

    result = read_json_file("protected.txt")

    assert result == []


@patch('utils.get_data_path', side_effect=mock_get_data_path)
def test_read_json_file_is_file_exception(mock_get_data_path):
    """Test when is_file() raises an exception"""
    mock_path = mock_get_data_path("error.txt")
    mock_path.exists.return_value = True
    mock_path.is_file.side_effect = OSError("Filesystem error")

    result = read_json_file("error.txt")

    assert result == []


@patch('utils.get_data_path', side_effect=mock_get_data_path)
def test_read_json_file_exists_exception(mock_get_data_path):
    """Test when exists() raises an exception"""
    mock_path = mock_get_data_path("error.txt")
    mock_path.exists.side_effect = OSError("Filesystem error")

    result = read_json_file("error.txt")

    assert result == []


# Test specific cases without decorator dependency
def test_read_json_file_empty_string():
    """Test with empty string filename (edge case)"""
    result = read_json_file("")

    assert isinstance(result, list)


# Test that function handles missing get_data_path gracefully
@patch('utils.get_data_path', side_effect=Exception("Module not found"))
def test_read_json_file_get_data_path_exception(mock_get_data_path):
    """Test when get_data_path itself raises an exception"""

    result = read_json_file("test.json")
    assert result == []