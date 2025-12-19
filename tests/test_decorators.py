"""
Tests for module decorators.py
"""

import os
from functools import wraps
from typing import Callable, Optional
from unittest.mock import Mock, patch

import pytest

from decorators import log, open_file_safely

'''Test functions for decorator @log'''


@log()
def successful_function(x: int, y: int) -> int:
    """Test function that always succeeds"""
    return x + y


@log()
def failing_function() -> None:
    """Test function that always fails"""
    raise ValueError("Test error message")


@log("test_log.txt")
def successful_function_with_file(x: int) -> int:
    """Test function with file logging"""
    return x * 2


@log("test_log.txt")
def failing_function_with_file() -> None:
    """Test function with file logging that fails"""
    raise RuntimeError("File logging error")


# Valid cases

def test_log_decorator_success_console(capsys):
    """Test successful function execution with console logging"""
    result = successful_function(5, 3)

    assert result == 8


def test_log_decorator_success_file():
    """Test successful function execution with file logging"""
    if os.path.exists("test_log.txt"):
        os.remove("test_log.txt")

    result = successful_function_with_file(10)

    assert result == 20

    with open("test_log.txt", "r", encoding="utf-8") as f:
        content = f.read()
        assert "successful_function_with_file successfully logged." in content


def test_log_decorator_preserves_function_metadata():
    """Test that decorator preserves original function metadata"""
    assert successful_function.__name__ == "successful_function"
    assert "Test function that always succeeds" in successful_function.__doc__


def test_log_decorator_with_different_arguments():
    """Test decorator with various argument types"""

    @log()
    def complex_function(a: int, b: str, c: list, d: dict = None) -> str:
        return f"{a} {b} {c} {d}"

    result = complex_function(1, "test", [1, 2, 3], {"key": "value"})
    assert result == "1 test [1, 2, 3] {'key': 'value'}"


# Edge cases
def test_log_decorator_empty_arguments():
    """Test decorator with function that has no arguments"""

    @log()
    def no_args_function() -> str:
        return "no args"

    result = no_args_function()
    assert result == "no args"


def test_log_decorator_keyword_arguments():
    """Test decorator with keyword arguments"""

    @log()
    def keyword_function(a: int, b: int = 10) -> int:
        return a + b

    result = keyword_function(5, b=15)
    assert result == 20


def test_log_decorator_none_filename(capsys):
    """Test decorator with explicit None filename (should use console)"""

    @log(None)
    def none_filename_function() -> str:
        return "test"

    result = none_filename_function()
    captured = capsys.readouterr()

    assert result == "test"
    assert "none_filename_function successfully logged." in captured.out


def test_log_decorator_multiple_calls_same_file():
    """Test multiple function calls writing to same file"""
    if os.path.exists("test_log.txt"):
        os.remove("test_log.txt")

    successful_function_with_file(1)
    successful_function_with_file(2)
    successful_function_with_file(3)

    with open("test_log.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert len(lines) == 3
        assert all("successful_function_with_file successfully logged." in line for line in lines)


# Invalid cases

def test_log_decorator_exception_handling_console(capsys):
    """Test exception handling with console logging"""
    with pytest.raises(ValueError, match="Test error message"):
        failing_function()

    captured = capsys.readouterr()
    assert "failing_function failed to log." in captured.out
    assert "ValueError: Test error message" in captured.out
    assert "inputs: (); {}" in captured.out


def test_log_decorator_exception_handling_file():
    """Test exception handling with file logging"""
    if os.path.exists("test_log.txt"):
        os.remove("test_log.txt")

    with pytest.raises(RuntimeError, match="File logging error"):
        failing_function_with_file()

    with open("test_log.txt", "r", encoding="utf-8") as f:
        content = f.read()
        assert "failing_function_with_file failed to log." in content
        assert "RuntimeError: File logging error" in content


def test_log_decorator_exception_with_arguments(capsys):
    """Test exception handling when function has arguments"""

    @log()
    def failing_with_args(x: int, y: str) -> None:
        raise TypeError(f"Error with {x} and {y}")

    with pytest.raises(TypeError):
        failing_with_args(10, "test")

    captured = capsys.readouterr()
    assert "failing_with_args failed to log." in captured.out
    assert "TypeError: Error with 10 and test" in captured.out
    assert "inputs: (10, 'test'); {}" in captured.out


def test_log_decorator_file_permission_error(monkeypatch):
    """Test behavior when file writing fails"""

    def mock_write(*args, **kwargs):
        raise PermissionError("Access denied")

    monkeypatch.setattr("builtins.open", mock_write)

    with pytest.raises(ValueError, match="Test error message"):
        failing_function()


# Cleanup

def teardown_module():
    """Clean up test files after tests"""
    if os.path.exists("test_log.txt"):
        os.remove("test_log.txt")


'''Test functions for decorator @open_file_safely'''


# Mock function to use with decorator
def sample_read_function(filename: str) -> list:
    """Sample function that would read a file and return data"""
    return ["data1", "data2", "data3"]


# Decorated function for testing
@open_file_safely
def decorated_read_function(filename: Optional[str] = None) -> list:
    """Decorated version of sample function"""
    return sample_read_function(filename)


# Valid cases
def test_open_file_safely_valid_file():
    """Test with valid existing non-empty file"""
    with patch('pathlib.Path.exists') as mock_exists, \
            patch('pathlib.Path.is_file') as mock_is_file, \
            patch('pathlib.Path.stat') as mock_stat:
        # Mock all checks to pass
        mock_exists.return_value = True
        mock_is_file.return_value = True
        mock_stat.return_value = Mock(st_size=100)  # Non-empty file

        # Mock the actual function
        mock_func = Mock(return_value=["test", "data"])
        decorated_func = open_file_safely(mock_func)

        result = decorated_func("valid_file.txt")

        # Should call the original function
        mock_func.assert_called_once_with("valid_file.txt")
        assert result == ["test", "data"]


def test_open_file_safely_returns_empty_list_on_none():
    """Test that returns empty list when filename is None"""
    mock_func = Mock(return_value=["data"])
    decorated_func = open_file_safely(mock_func)

    result = decorated_func(None)


# Edge cases
def test_open_file_safely_file_does_not_exist():
    """Test when file does not exist"""
    with patch('pathlib.Path.exists') as mock_exists:
        mock_exists.return_value = False

        mock_func = Mock(return_value=["data"])
        decorated_func = open_file_safely(mock_func)

        result = decorated_func("nonexistent.txt")

        mock_func.assert_not_called()
        assert result == []


def test_open_file_safely_path_is_directory_not_file():
    """Test when path exists but is a directory, not a file"""
    with patch('pathlib.Path.exists') as mock_exists, \
            patch('pathlib.Path.is_file') as mock_is_file:
        mock_exists.return_value = True
        mock_is_file.return_value = False  # It's a directory

        mock_func = Mock(return_value=["data"])
        decorated_func = open_file_safely(mock_func)

        result = decorated_func("/some/directory")

        mock_func.assert_not_called()
        assert result == []


def test_open_file_safely_empty_file():
    """Test when file exists but is empty (size = 0)"""
    with patch('pathlib.Path.exists') as mock_exists, \
            patch('pathlib.Path.is_file') as mock_is_file, \
            patch('pathlib.Path.stat') as mock_stat:
        mock_exists.return_value = True
        mock_is_file.return_value = True
        mock_stat.return_value = Mock(st_size=0)  # Empty file

        mock_func = Mock(return_value=["data"])
        decorated_func = open_file_safely(mock_func)

        result = decorated_func("empty.txt")

        mock_func.assert_not_called()
        assert result == []


def test_open_file_safely_with_empty_string_filename():
    """Test with empty string as filename"""
    mock_func = Mock(return_value=["data"])
    decorated_func = open_file_safely(mock_func)

    result = decorated_func("")

    # Empty string is truthy, so will check Path("") which doesn't exist
    with patch('pathlib.Path.exists') as mock_exists:
        mock_exists.return_value = False
        mock_func.assert_not_called()

    assert result == []


# Test with actual decorated function
def test_decorated_read_function_valid():
    """Test the actual decorated function with valid file"""
    with patch('pathlib.Path.exists') as mock_exists, \
            patch('pathlib.Path.is_file') as mock_is_file, \
            patch('pathlib.Path.stat') as mock_stat, \
            patch.object(__import__(__name__), 'sample_read_function') as mock_read:
        mock_exists.return_value = True
        mock_is_file.return_value = True
        mock_stat.return_value = Mock(st_size=100)
        mock_read.return_value = ["real", "data"]

        result = decorated_read_function("real_file.txt")

        mock_read.assert_called_once_with("real_file.txt")
        assert result == ["real", "data"]


def test_decorated_read_function_invalid():
    """Test the actual decorated function with invalid file"""
    with patch('pathlib.Path.exists') as mock_exists:
        mock_exists.return_value = False

        result = decorated_read_function("fake_file.txt")

        assert result == []


# Test with different return types
def test_open_file_safely_with_different_return_types():
    """Test that decorator handles different return types from wrapped function"""

    @open_file_safely
    def return_dict(filename: str) -> dict:
        return {"key": "value"}

    @open_file_safely
    def return_string(filename: str) -> str:
        return "result"

    with patch('pathlib.Path.exists') as mock_exists, \
            patch('pathlib.Path.is_file') as mock_is_file, \
            patch('pathlib.Path.stat') as mock_stat:
        mock_exists.return_value = True
        mock_is_file.return_value = True
        mock_stat.return_value = Mock(st_size=100)

        dict_result = return_dict("test.txt")
        string_result = return_string("test.txt")

        assert dict_result == {"key": "value"}
        assert string_result == "result"


def test_open_file_safely_invalid_path_object_creation():
    """Test when Path() constructor itself raises an exception"""
    with patch('pathlib.Path') as mock_path_class:
        mock_path_class.side_effect = ValueError("Invalid path")

        mock_func = Mock(return_value=["data"])
        decorated_func = open_file_safely(mock_func)

        # Should handle exception from Path constructor
        result = decorated_func("invalid:\0path.txt")

        mock_func.assert_not_called()
        assert result == []
