import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
import io
from table_readers import read_transactions_csv, read_transactions_excel


# Test data
CSV_CONTENT = """id;state;date;amount;currency_name;currency_code;from;to;description
650703;EXECUTED;2023-09-05T11:30:32Z;16210;Sol;PEN;Счет 58803664561298323391;Счет 39745660563456619397;Перевод организации
3598919;EXECUTED;2020-12-06T23:00:58Z;29740;Peso;COP;Discover 3172601889670065;Discover 0720428384694643;Перевод с карты на карту
593027;CANCELED;2023-07-22T05:02:01Z;30368;Shilling;TZS;Visa 1959232722494097;Visa 6804119550473710;Перевод с карты на карту
"""

CSV_CONTENT_EMPTY = """id;state;date;amount;currency_name;currency_code;from;to;description
"""

CSV_CONTENT_SINGLE = """id;state;date;amount;currency_name;currency_code;from;to;description
650703;EXECUTED;2023-09-05T11:30:32Z;16210;Sol;PEN;Счет 58803664561298323391;Счет 39745660563456619397;Перевод организации
"""

# Test data for creating Excel files
EXCEL_DATA = [
    {'id': 650703, 'state': 'EXECUTED', 'date': '2023-09-05T11:30:32Z', 'amount': 16210,
     'currency_name': 'Sol', 'currency_code': 'PEN',
     'from': 'Счет 58803664561298323391', 'to': 'Счет 39745660563456619397',
     'description': 'Перевод организации'},
    {'id': 3598919, 'state': 'EXECUTED', 'date': '2020-12-06T23:00:58Z', 'amount': 29740,
     'currency_name': 'Peso', 'currency_code': 'COP',
     'from': 'Discover 3172601889670065', 'to': 'Discover 0720428384694643',
     'description': 'Перевод с карты на карту'},
    {'id': 593027, 'state': 'CANCELED', 'date': '2023-07-22T05:02:01Z', 'amount': 30368,
     'currency_name': 'Shilling', 'currency_code': 'TZS',
     'from': 'Visa 1959232722494097', 'to': 'Visa 6804119550473710',
     'description': 'Перевод с карты на карту'}
]

# Helper function to create mock DataFrame
def create_mock_dataframe(csv_content):
    """Create a mock DataFrame with proper to_dict method"""
    # Create real DataFrame from CSV content
    real_df = pd.read_csv(io.StringIO(csv_content), delimiter=';')

    # Create mock DataFrame
    mock_df = MagicMock()
    mock_df.to_dict.return_value = real_df.to_dict("records")
    return mock_df


# Valid cases
def test_read_transactions_csv_valid_file():
    """Test reading valid CSV file"""
    # Create mock DataFrame
    mock_df = create_mock_dataframe(CSV_CONTENT)

    with patch('pandas.read_csv', return_value=mock_df) as mock_read_csv:
        result = read_transactions_csv("transactions.csv")

        # Check pandas.read_csv was called correctly
        mock_read_csv.assert_called_once_with("transactions.csv", delimiter=";")

        # Check that to_dict was called with correct argument
        mock_df.to_dict.assert_called_once_with("records")

        # Check result
        assert isinstance(result, list)
        assert len(result) == 3
        assert all(isinstance(item, dict) for item in result)

        # Check values in result
        # Note: to_dict returns actual data, so we can check it
        assert result[0]['id'] == 650703
        assert result[0]['state'] == 'EXECUTED'
        assert result[0]['currency_code'] == 'PEN'
        assert result[0]['description'] == 'Перевод организации'


def test_read_transactions_csv_single_transaction():
    """Test reading CSV file with single transaction"""
    # Create mock DataFrame
    mock_df = create_mock_dataframe(CSV_CONTENT_SINGLE)

    with patch('pandas.read_csv', return_value=mock_df):
        result = read_transactions_csv("single.csv")

        assert len(result) == 1
        assert result[0]['id'] == 650703
        assert result[0]['amount'] == 16210


def test_read_transactions_csv_empty_file():
    """Test reading empty CSV file (only headers)"""
    # Create mock DataFrame for empty file
    real_df = pd.read_csv(io.StringIO(CSV_CONTENT_EMPTY), delimiter=';')
    mock_df = MagicMock()
    mock_df.to_dict.return_value = real_df.to_dict("records")  # Returns empty list

    with patch('pandas.read_csv', return_value=mock_df):
        result = read_transactions_csv("empty.csv")

        assert result == []
        assert isinstance(result, list)


# Alternative approach: mock the entire chain
def test_read_transactions_csv_mock_chain():
    """Test using mocked chain of calls"""
    with patch('pandas.read_csv') as mock_read_csv:
        # Create a mock DataFrame
        mock_df = MagicMock()

        # Setup to_dict to return specific data
        expected_result = [
            {'id': 650703, 'state': 'EXECUTED', 'amount': 16210},
            {'id': 3598919, 'state': 'EXECUTED', 'amount': 29740}
        ]
        mock_df.to_dict.return_value = expected_result

        # Setup read_csv to return the mock DataFrame
        mock_read_csv.return_value = mock_df

        result = read_transactions_csv("test.csv")

        # Verify calls
        mock_read_csv.assert_called_once_with("test.csv", delimiter=";")
        mock_df.to_dict.assert_called_once_with("records")

        # Verify result
        assert result == expected_result
        assert len(result) == 2
        assert result[0]['id'] == 650703


# Test with actual pandas (integration style)
def test_read_transactions_csv_integration(tmp_path):
    """Integration test with actual file"""
    # Create a temporary CSV file
    csv_file = tmp_path / "transactions.csv"
    csv_file.write_text(CSV_CONTENT_SINGLE, encoding='utf-8')

    # Call the function with real file
    result = read_transactions_csv(str(csv_file))

    # Verify result
    assert len(result) == 1
    assert result[0]['id'] == 650703
    assert result[0]['state'] == 'EXECUTED'
    assert result[0]['description'] == 'Перевод организации'


# Test error cases
def test_read_transactions_csv_file_not_found():
    """Test when file doesn't exist"""
    with patch('pandas.read_csv') as mock_read_csv:
        mock_read_csv.side_effect = FileNotFoundError("File not found")

        with pytest.raises(FileNotFoundError, match="File not found"):
            read_transactions_csv("nonexistent.csv")

        mock_read_csv.assert_called_once_with("nonexistent.csv", delimiter=";")


def test_read_transactions_csv_invalid_delimiter():
    """Test with wrong delimiter (though function always uses ;)"""
    with patch('pandas.read_csv') as mock_read_csv:
        mock_read_csv.side_effect = pd.errors.ParserError("Error tokenizing data")

        with pytest.raises(pd.errors.ParserError):
            read_transactions_csv("invalid.csv")

        mock_read_csv.assert_called_once_with("invalid.csv", delimiter=";")


# Test that function preserves all columns
def test_read_transactions_csv_preserves_all_columns():
    """Test that all CSV columns are preserved in result"""
    csv_with_all_columns = """id;state;date;amount;currency_name;currency_code;from;to;description;extra_col
1;EXECUTED;2023-01-01T00:00:00Z;100;Euro;EUR;From;To;Desc;Extra
"""

    real_df = pd.read_csv(io.StringIO(csv_with_all_columns), delimiter=';')
    mock_df = MagicMock()
    mock_df.to_dict.return_value = real_df.to_dict("records")

    with patch('pandas.read_csv', return_value=mock_df):
        result = read_transactions_csv("with_extra.csv")

        assert len(result) == 1
        assert 'extra_col' in result[0]
        assert result[0]['extra_col'] == 'Extra'
        assert len(result[0].keys()) == 10  # Все 10 колонок


# Parameterized test
@pytest.mark.parametrize("csv_content,expected_count", [
    (CSV_CONTENT, 3),
    (CSV_CONTENT_SINGLE, 1),
    (CSV_CONTENT_EMPTY, 0),
])
def test_read_transactions_csv_parameterized(csv_content, expected_count):
    """Parameterized test for different CSV contents"""
    real_df = pd.read_csv(io.StringIO(csv_content), delimiter=';')
    mock_df = MagicMock()
    mock_df.to_dict.return_value = real_df.to_dict("records")

    with patch('pandas.read_csv', return_value=mock_df):
        result = read_transactions_csv("test.csv")

        assert len(result) == expected_count
        mock_df.to_dict.assert_called_once_with("records")


# Test with different data types
def test_read_transactions_csv_mixed_data_types():
    """Test CSV with mixed data types"""
    csv_mixed = """id;amount;is_active;name;price
1;100;true;Product A;19.99
2;200;false;Product B;29.50
"""

    real_df = pd.read_csv(io.StringIO(csv_mixed), delimiter=';')
    mock_df = MagicMock()
    mock_df.to_dict.return_value = real_df.to_dict("records")

    with patch('pandas.read_csv', return_value=mock_df):
        result = read_transactions_csv("mixed.csv")

        assert len(result) == 2
        # Check that different types are preserved
        assert result[0]['id'] == 1
        assert result[0]['amount'] == 100
        assert result[0]['is_active'] is True  # pandas converts 'true' to True
        assert result[0]['price'] == 19.99


# Helper function to create mock DataFrame
def create_mock_excel_dataframe(data=None):
    """Create a mock DataFrame for Excel data"""
    if data is None:
        data = EXCEL_DATA

    # Create real DataFrame from data
    real_df = pd.DataFrame(data)

    # Create mock DataFrame
    mock_df = MagicMock()
    mock_df.to_dict.return_value = real_df.to_dict("records")
    return mock_df, real_df


# Valid cases
def test_read_transactions_excel_valid_file():
    """Test reading valid Excel file"""
    # Create mock DataFrame
    mock_df, real_df = create_mock_excel_dataframe()

    with patch('pandas.read_excel', return_value=mock_df) as mock_read_excel:
        result = read_transactions_excel("transactions.xlsx")

        # Check pandas.read_excel was called correctly
        mock_read_excel.assert_called_once_with("transactions.xlsx")

        # Check that to_dict was called with correct argument
        mock_df.to_dict.assert_called_once_with("records")

        # Check result
        assert isinstance(result, list)
        assert len(result) == 3
        assert all(isinstance(item, dict) for item in result)

        # Check first transaction
        assert result[0]['id'] == 650703
        assert result[0]['state'] == 'EXECUTED'
        assert result[0]['currency_code'] == 'PEN'
        assert result[0]['description'] == 'Перевод организации'


def test_read_transactions_excel_single_transaction():
    """Test reading Excel file with single transaction"""
    single_data = [EXCEL_DATA[0]]  # Just the first transaction

    mock_df, real_df = create_mock_excel_dataframe(single_data)

    with patch('pandas.read_excel', return_value=mock_df):
        result = read_transactions_excel("single.xlsx")

        assert len(result) == 1
        assert result[0]['id'] == 650703
        assert result[0]['amount'] == 16210
        assert result[0]['from'] == 'Счет 58803664561298323391'


def test_read_transactions_excel_empty_file():
    """Test reading empty Excel file"""
    # Create mock DataFrame for empty data
    mock_df = MagicMock()
    mock_df.to_dict.return_value = []

    with patch('pandas.read_excel', return_value=mock_df):
        result = read_transactions_excel("empty.xlsx")

        assert result == []
        assert isinstance(result, list)


def test_read_transactions_excel_with_special_characters():
    """Test reading Excel with special characters"""
    special_data = [{
        'id': 1,
        'description': 'Payment with , and ; and "quotes" and эмодзи 😀',
        'amount': 100.50,
        'state': 'EXECUTED'
    }]

    mock_df, real_df = create_mock_excel_dataframe(special_data)

    with patch('pandas.read_excel', return_value=mock_df):
        result = read_transactions_excel("special.xlsx")

        assert len(result) == 1
        assert result[0]['id'] == 1
        assert result[0]['description'] == 'Payment with , and ; and "quotes" and эмодзи 😀'
        assert result[0]['amount'] == 100.50


# Edge cases
def test_read_transactions_excel_with_different_sheet_name():
    """Test that function uses default sheet (first sheet)"""
    mock_df, real_df = create_mock_excel_dataframe()

    with patch('pandas.read_excel') as mock_read_excel:
        mock_read_excel.return_value = mock_df

        result = read_transactions_excel("test.xlsx")

        # Should call read_excel without sheet_name parameter
        mock_read_excel.assert_called_once_with("test.xlsx")

        # Verify to_dict called
        mock_df.to_dict.assert_called_once_with("records")


def test_read_transactions_excel_with_numeric_types():
    """Test Excel with various numeric types"""
    numeric_data = [
        {'id': 1, 'int_value': 100, 'float_value': 100.50, 'scientific': 1.23e6},
        {'id': 2, 'int_value': 200, 'float_value': 200.75, 'scientific': 4.56e-3}
    ]

    mock_df, real_df = create_mock_excel_dataframe(numeric_data)

    with patch('pandas.read_excel', return_value=mock_df):
        result = read_transactions_excel("numeric.xlsx")

        assert len(result) == 2
        assert result[0]['int_value'] == 100
        assert result[0]['float_value'] == 100.50
        assert result[0]['scientific'] == 1230000.0  # 1.23e6
        assert result[1]['scientific'] == 0.00456  # 4.56e-3


def test_read_transactions_excel_with_missing_values():
    """Test Excel with missing/NaN values"""
    data_with_nan = [
        {'id': 1, 'amount': 100, 'description': 'Complete'},
        {'id': 2, 'amount': None, 'description': None},  # None values
        {'id': 3, 'amount': 300, 'description': 'Another'}
    ]

    # Create DataFrame and convert to dict (pandas handles NaN)
    real_df = pd.DataFrame(data_with_nan)
    mock_df = MagicMock()
    mock_df.to_dict.return_value = real_df.to_dict("records")

    with patch('pandas.read_excel', return_value=mock_df):
        result = read_transactions_excel("with_nan.xlsx")

        assert len(result) == 3
        assert result[0]['amount'] == 100
        assert pd.isna(result[1]['amount'])  # Should be NaN
        assert pd.isna(result[1]['description'])  # Should be NaN
        assert result[2]['amount'] == 300


# Invalid cases
def test_read_transactions_excel_file_not_found():
    """Test when Excel file doesn't exist"""
    with patch('pandas.read_excel') as mock_read_excel:
        mock_read_excel.side_effect = FileNotFoundError("File not found")

        with pytest.raises(FileNotFoundError, match="File not found"):
            read_transactions_excel("nonexistent.xlsx")

        mock_read_excel.assert_called_once_with("nonexistent.xlsx")


def test_read_transactions_excel_permission_error():
    """Test when no permission to read Excel file"""
    with patch('pandas.read_excel') as mock_read_excel:
        mock_read_excel.side_effect = PermissionError("Permission denied")

        with pytest.raises(PermissionError, match="Permission denied"):
            read_transactions_excel("protected.xlsx")


def test_read_transactions_excel_empty_string_path():
    """Test with empty string as file path"""
    with patch('pandas.read_excel') as mock_read_excel:
        mock_read_excel.side_effect = FileNotFoundError("File b'' does not exist")

        with pytest.raises(FileNotFoundError):
            read_transactions_excel("")


def test_read_transactions_excel_corrupted_file():
    """Test when Excel file is corrupted"""
    with patch('pandas.read_excel') as mock_read_excel:
        mock_read_excel.side_effect = ValueError("File is not a recognized excel file")

        with pytest.raises(ValueError, match="File is not a recognized excel file"):
            read_transactions_excel("corrupted.xlsx")


def test_read_transactions_excel_invalid_excel_format():
    """Test with invalid Excel format"""
    with patch('pandas.read_excel') as mock_read_excel:
        mock_read_excel.side_effect = ImportError("Missing optional dependency 'openpyxl'")

        with pytest.raises(ImportError, match="Missing optional dependency"):
            read_transactions_excel("test.xlsx")


# Parameterized tests
@pytest.mark.parametrize("data,expected_count", [
    (EXCEL_DATA, 3),
    ([EXCEL_DATA[0]], 1),
    ([], 0),
])
def test_read_transactions_excel_parameterized(data, expected_count):
    """Parameterized test for different data sizes"""
    mock_df, real_df = create_mock_excel_dataframe(data)

    with patch('pandas.read_excel', return_value=mock_df):
        result = read_transactions_excel("test.xlsx")

        assert len(result) == expected_count
        mock_df.to_dict.assert_called_once_with("records")


# Test with different file extensions
@pytest.mark.parametrize("filename", [
    "transactions.xlsx",
    "transactions.xls",
    "transactions.xlsm",
    "transactions.xlsb",
])
def test_read_transactions_excel_different_extensions(filename):
    """Test with different Excel file extensions"""
    mock_df, real_df = create_mock_excel_dataframe()

    with patch('pandas.read_excel', return_value=mock_df) as mock_read_excel:
        result = read_transactions_excel(filename)

        mock_read_excel.assert_called_once_with(filename)
        assert len(result) == 3


# Integration test with actual Excel file (optional)
def test_read_transactions_excel_integration(tmp_path):
    """Integration test with actual Excel file"""
    # Create a temporary Excel file
    excel_file = tmp_path / "transactions.xlsx"

    # Create DataFrame and save to Excel
    df = pd.DataFrame(EXCEL_DATA[:1])  # Just first transaction
    df.to_excel(excel_file, index=False)

    # Call the function with real file
    result = read_transactions_excel(str(excel_file))

    # Verify result
    assert len(result) == 1
    assert result[0]['id'] == 650703
    assert result[0]['state'] == 'EXECUTED'
    assert result[0]['description'] == 'Перевод организации'


# Test that function preserves column order
def test_read_transactions_excel_preserves_column_order():
    """Test that column order is preserved from Excel"""
    data_with_specific_order = [
        {'Z_column': 'z', 'A_column': 'a', 'M_column': 'm'},
        {'Z_column': 'z2', 'A_column': 'a2', 'M_column': 'm2'}
    ]

    real_df = pd.DataFrame(data_with_specific_order)
    mock_df = MagicMock()
    mock_df.to_dict.return_value = real_df.to_dict("records")

    with patch('pandas.read_excel', return_value=mock_df):
        result = read_transactions_excel("order_test.xlsx")

        # Check column order in first result
        columns = list(result[0].keys())
        # Order should match DataFrame columns
        assert columns == ['Z_column', 'A_column', 'M_column']


# Test with large Excel file simulation
def test_read_transactions_excel_large_file():
    """Test with simulation of large Excel file"""
    # Create data for 1000 records
    large_data = []
    for i in range(1000):
        large_data.append({
            'id': i,
            'amount': i * 100,
            'description': f'Transaction {i}',
            'state': 'EXECUTED' if i % 2 == 0 else 'CANCELED'
        })

    mock_df, real_df = create_mock_excel_dataframe(large_data)

    with patch('pandas.read_excel', return_value=mock_df):
        result = read_transactions_excel("large.xlsx")

        assert len(result) == 1000
        # Check first and last records
        assert result[0]['id'] == 0
        assert result[0]['state'] == 'EXECUTED'
        assert result[999]['id'] == 999
        assert result[999]['state'] == 'CANCELED'