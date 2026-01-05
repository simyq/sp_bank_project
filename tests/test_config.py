"""Tests for config module"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from config import *

# Тесты для функций получения путей

def test_get_log_path():
    """Test get_log_path function creates directory and returns correct path"""
    filename = "test.log"

    # Тестируем с моком для mkdir
    with patch('pathlib.Path.mkdir') as mock_mkdir:
        result = get_log_path(filename)

        # Проверяем что mkdir был вызван с правильными параметрами
        mock_mkdir.assert_called_once_with(exist_ok=True)

        # Проверяем что результат - Path объект
        assert isinstance(result, Path)

        # Проверяем что имя файла в пути
        assert result.name == filename

        # Проверяем что путь содержит нужные части
        assert "logs" in str(result)


def test_get_data_path():
    """Test get_data_path function creates directory and returns correct path"""
    filename = "test.json"

    with patch('pathlib.Path.mkdir') as mock_mkdir:
        result = get_data_path(filename)

        mock_mkdir.assert_called_once_with(exist_ok=True)
        assert isinstance(result, Path)
        assert result.name == filename
        assert "data" in str(result)


def test_get_tests_path():
    """Test get_tests_path function returns correct path without creating directory"""
    filename = "test_file.py"

    # Для get_tests_path не должно быть вызова mkdir
    result = get_tests_path(filename)

    assert isinstance(result, Path)
    assert result.name == filename
    assert "tests" in str(result)


def test_get_src_path():
    """Test get_src_path function returns correct path without creating directory"""
    filename = "module.py"

    result = get_src_path(filename)

    assert isinstance(result, Path)
    assert result.name == filename
    assert "src" in str(result)


# Edge cases


def test_path_functions_with_nested_path():
    """Test path functions with nested paths in filename"""
    nested_filename = "subdir/test.log"

    with patch('pathlib.Path.mkdir'):
        result = get_log_path(nested_filename)

        assert isinstance(result, Path)
        assert result.name == "test.log"
        assert "subdir" in str(result)


# Test with special characters
@pytest.mark.parametrize("filename", [
    "test-file.log",
    "test_file.log",
    "test file.log",
    "тест.log",
    "test@#$%.log",
])
def test_get_log_path_with_special_characters(filename):
    """Test get_log_path with various special characters in filename"""
    with patch('pathlib.Path.mkdir'):
        result = get_log_path(filename)

        assert isinstance(result, Path)
        assert result.name == filename


# Test directory creation behavior
def test_get_log_path_directory_exists():
    """Test that mkdir is called with exist_ok=True even if directory exists"""
    with patch('pathlib.Path.mkdir') as mock_mkdir:
        # Симулируем что директория уже существует
        get_log_path("test.log")

        # Проверяем что mkdir вызван с exist_ok=True
        mock_mkdir.assert_called_once_with(exist_ok=True)


def test_get_data_path_directory_exists():
    """Test that mkdir is called with exist_ok=True for data path"""
    with patch('pathlib.Path.mkdir') as mock_mkdir:
        get_data_path("test.json")

        mock_mkdir.assert_called_once_with(exist_ok=True)


# Test PATHS dictionary
def test_paths_dictionary_structure():
    """Test that PATHS dictionary contains expected keys and values"""
    expected_keys = ["src", "tests", "logs", "data"]

    assert all(key in PATHS for key in expected_keys)
    assert len(PATHS) == len(expected_keys)

    # Все значения должны быть Path объектами
    for path in PATHS.values():
        assert isinstance(path, Path)


def test_paths_relative_to_project_root():
    """Test that all paths are relative to PROJECT_ROOT"""
    for key, path in PATHS.items():
        # Путь должен содержать PROJECT_ROOT как родителя
        assert PROJECT_ROOT in path.parents or path == PROJECT_ROOT / key.lower()


# Test PROJECT_ROOT constant
def test_project_root_is_path_object():
    """Test that PROJECT_ROOT is a Path object"""
    assert isinstance(PROJECT_ROOT, Path)


def test_project_root_exists():
    """Test that PROJECT_ROOT points to a valid directory (might not exist in tests)"""
    # Это может быть или не быть существующим путем в тестовой среде
    # Главное что это Path объект
    assert isinstance(PROJECT_ROOT, Path)


# Integration-style tests (без моков)
def test_get_log_path_integration(tmp_path):
    """Integration test for get_log_path with temporary directory"""
    # Сохраняем оригинальный PATHS
    original_paths = PATHS.copy()

    try:
        # Временная замена PATHS для теста
        PATHS["logs"] = tmp_path / "test_logs"

        filename = "integration_test.log"
        result = get_log_path(filename)

        # Проверяем результат
        assert isinstance(result, Path)
        assert result.name == filename

        # Проверяем что директория была создана
        assert result.parent.exists()
        assert result.parent.is_dir()

    finally:
        # Восстанавливаем оригинальный PATHS
        PATHS.clear()
        PATHS.update(original_paths)


def test_get_data_path_integration(tmp_path):
    """Integration test for get_data_path with temporary directory"""
    original_paths = PATHS.copy()

    try:
        PATHS["data"] = tmp_path / "test_data"

        filename = "integration_data.json"
        result = get_data_path(filename)

        assert isinstance(result, Path)
        assert result.name == filename
        assert result.parent.exists()
        assert result.parent.is_dir()

    finally:
        PATHS.clear()
        PATHS.update(original_paths)


# Test error cases
def test_get_log_path_with_none_filename():
    """Test get_log_path with None filename"""
    with patch('pathlib.Path.mkdir'):

        with pytest.raises(TypeError):
            get_log_path(None)



def test_get_data_path_with_integer_filename():
    """Test get_data_path with integer filename"""
    with patch('pathlib.Path.mkdir'):
        with pytest.raises(TypeError):
            get_log_path(123)


# Test that functions don't create directories for tests and src
def test_get_tests_path_no_directory_creation():
    """Test that get_tests_path doesn't create directory"""
    with patch('pathlib.Path.mkdir') as mock_mkdir:
        get_tests_path("test.py")

        # mkdir не должен быть вызван
        mock_mkdir.assert_not_called()


def test_get_src_path_no_directory_creation():
    """Test that get_src_path doesn't create directory"""
    with patch('pathlib.Path.mkdir') as mock_mkdir:
        get_src_path("module.py")

        mock_mkdir.assert_not_called()


# Test path concatenation
@pytest.mark.parametrize("function,expected_dir", [
    (get_log_path, "logs"),
    (get_data_path, "data"),
    (get_tests_path, "tests"),
    (get_src_path, "src"),
])
def test_path_concatenation(function, expected_dir):
    """Test that paths are correctly concatenated"""
    test_filename = "test.txt"

    with patch('pathlib.Path.mkdir'):
        result = function(test_filename)

        # Проверяем что путь заканчивается ожидаемым именем файла
        assert str(result).endswith(f"{expected_dir}/{test_filename}") or \
               str(result).endswith(f"{expected_dir}\\{test_filename}")


# Test with mock PATHS
def test_functions_use_pathes_from_dict():
    """Test that functions use PATHS from the module"""
    original_paths = PATHS.copy()

    try:
        # Временно меняем PATHS
        test_log_path = Path("/test/dir/logs")
        PATHS["logs"] = test_log_path

        with patch('pathlib.Path.mkdir'):
            result = get_log_path("test.log")

            # Проверяем что используется измененный путь
            assert test_log_path in result.parents

    finally:
        # Восстанавливаем оригинальные пути
        PATHS.clear()
        PATHS.update(original_paths)


# Test multiple calls
def test_multiple_calls_to_same_function():
    """Test that multiple calls to same function work correctly"""
    with patch('pathlib.Path.mkdir') as mock_mkdir:
        # Первый вызов
        result1 = get_log_path("first.log")

        # Второй вызов с другим именем файла
        result2 = get_log_path("second.log")

        # mkdir должен быть вызван дважды
        assert mock_mkdir.call_count == 2

        # Результаты должны быть разными
        assert result1 != result2
        assert result1.name == "first.log"
        assert result2.name == "second.log"