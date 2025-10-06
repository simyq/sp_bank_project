"""
Tests for module decorators.py
"""

import pytest
import os

from decorators import log

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