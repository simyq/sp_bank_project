"""
Fixtures functions for testing
"""

import pytest

'''
For test_masks.py
'''

# Valid cases fixtures


@pytest.fixture(params=[("1234567890123456", "1234 56** **** 3456"),
                        ("7000792289606361", "7000 79** **** 6361"),
                        ("0000000000000000", "0000 00** **** 0000"),
                        ("9999999999999999", "9999 99** **** 9999"),
                        ("4111111111111111", "4111 11** **** 1111"),
                        ("5500000000000004", "5500 00** **** 0004"),])
def valid_card_data(request):
    """Returns tuple (card number, expected result)"""
    return request.param


@pytest.fixture(params=[("73654108430135874305", "**4305"),
                        ("12345678901234567890", "**7890"),
                        ("00000000000000000000", "**0000"),
                        ("99999999999999999999", "**9999"),
                        ("40817810099910004351", "**4351"),])
def valid_account_data(request):
    """Returns tuple (account number, expected result)"""
    return request.param


# Invalid cases fixtures (raise Exception)


@pytest.fixture(params=[{1: 1}, {1, 2}, None, False, 123])
def invalid_data_type(request):
    """Returns parameter of wrong type"""
    return request.param


# Edge and problematic cases (short or long strings, list or tuple type given)
# No Exception raising, but invalid outcome occur


@pytest.fixture(params=[("12345678901234567", "1234 56** **** 4567"),
                        ("123456789012345678", "1234 56** **** 5678"),
                        ("abcdefghijklmnop", "abcd ef** **** mnop"),
                        ("1234-5678-9012-3456", "1234 -5** **** 3456"),
                        ("123", "123 ** **** 123"),
                        ("", " ** **** "),
                        ([1, 2, 3], '[1, 2, 3] []** **** [1, 2, 3]')])
def problematic_card_data(request):
    return request.param


@pytest.fixture(params=[("123456789012345678901", "**8901"),
                        ("a" * 25, "**" + "a" * 4),
                        ("abcdefghijklmnopqrst", "**qrst"),
                        ("1234-5678-9012-3456-78", "**6-78"),
                        ("123", "**123"),
                        ("", "**"),
                        ([1, 2, 3], '**[1, 2, 3]')])
def problematic_account_data(request):
    return request.param


'''
For test_widget.py
'''

# Valid bank data strings


@pytest.fixture(params=[
    ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
    ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361"),
    ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),
    ("счет 73654108430135874305", "Счет **4305"),
    ("Счёт 12345678901234567890", "Счёт **7890"),
    ("Счет 00000000000000000000", "Счет **0000")
])
def valid_bank_data(request):
    """Returns tuple (bank data string, expected masked result)"""
    return request.param


# Invalid types


@pytest.fixture(params=[123, None, False, [1, 2, 3], {"card": "1234567890123456"}, 45.67])
def invalid_bank_data_type(request):
    """Returns invalid data types"""
    return request.param


# Invalid string formats


@pytest.fixture(params=[
    "",
    "   ",
    "Visa",
    "Visa 123",
    "Visa 12345678901234567",
    "Visa abcdefghijklmnop",
    "счет 123",
    "счет 123456789012345678901",
    "счет abcdefghijklmnopqrst",
    "UnknownType 1234567890123456",
    "Карта 1234567890123456",
    "Account 73654108430135874305",
])
def invalid_bank_data_format(request):
    """Returns invalid bank data strings"""
    return request.param


# Edge cases


@pytest.fixture(params=[
    ("  Visa  7000792289606361  ", "Visa 7000 79** **** 6361"),
    ("счет   73654108430135874305   ", "Счет **4305"),
    ("VISA 7000792289606361", "Visa 7000 79** **** 6361"),
    ("VISa 7000792289606361", "Visa 7000 79** **** 6361"),
    ("СЧЕТ 73654108430135874305", "Счет **4305"),
    ("СчЁт 73654108430135874305", "Счёт **4305"),
    ("vIsA pLaTiNuM 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
])
def edge_case_bank_data(request):
    """Returns edge cases with expected results"""
    return request.param


'''
Fixtures for processing.py tests
'''

# Basic tests data


@pytest.fixture
def sample_transactions():
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 615064592, 'state': 'PENDING', 'date': '2018-11-15T09:22:34.520552'}
    ]


# FIXTURES FOR filter_by_state

# Valid cases for filter_by_state


@pytest.fixture(params=[
    ('EXECUTED', [41428829, 939719570]),
    ('CANCELED', [594226727, 615064591]),
    ('PENDING', [615064592])
])
def valid_filter_state_data(request):
    return request.param


# Invalid cases for filter_by_state


@pytest.fixture(params=[
    'UNKNOWN',
    'executed',
    '',
    '123'
])
def invalid_filter_state_data(request):
    return request.param


# Edge cases for filter_by_state (empty list, single parameter, all parameters)


@pytest.fixture(params=[
    ([], 'EXECUTED'),
    ([{'id': 1, 'state': 'EXECUTED', 'date': '2023-01-01T00:00:00'}], 'EXECUTED'),
    ([{'id': 1, 'state': 'EXECUTED', 'date': '2023-01-01T00:00:00'},
      {'id': 2, 'state': 'EXECUTED', 'date': '2023-01-02T00:00:00'}], 'EXECUTED')
])
def edge_filter_state_data(request):
    return request.param


# FIXTURES FOR sort_by_date

# Valid cases for sort_by_date


@pytest.fixture(params=[
    (True, '2019-07-03T18:35:29.512364'),
    (False, '2018-06-30T02:08:58.425572')
])
def valid_sort_date_data(request):
    return request.param


# Invalid cases for sort_by_date (incorrect sorting parameter)


@pytest.fixture(params=['invalid', 123, None])
def invalid_sort_date_param(request):
    return request.param


# Edge cases for sort_by_date (empty list, single item, same dates)


@pytest.fixture(params=[
    [],
    [{'id': 1, 'state': 'EXECUTED', 'date': '2023-01-01T00:00:00'}],
    [{'id': 1, 'state': 'EXECUTED', 'date': '2023-01-01T12:00:00'},
     {'id': 2, 'state': 'CANCELED', 'date': '2023-01-01T12:00:00'},
     {'id': 3, 'state': 'EXECUTED', 'date': '2023-01-01T12:00:00'}]
])
def edge_sort_date_data(request):
    return request.param


'''
Fixtures for test_generators.py
'''

@pytest.fixture
def sample_gen_transactions():
    """Fixture with transactions data"""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2018-01-01T00:00:00.000000",
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "name": "US Dollar",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 10000000000000000001",
            "to": "Счет 20000000000000000002"
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2018-01-02T00:00:00.000000",
            "operationAmount": {
                "amount": "200.00",
                "currency": {
                    "name": "Euro",
                    "code": "EUR"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 10000000000000000001",
            "to": "Счет 30000000000000000003"
        },
        {
            "id": 3,
            "state": "CANCELED",
            "date": "2018-01-03T00:00:00.000000",
            "operationAmount": {
                "amount": "300.00",
                "currency": {
                    "name": "US Dollar",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Карта 1000000000000001",
            "to": "Карта 2000000000000002"
        },
        {
            "id": 4,
            "state": "EXECUTED",
            "date": "2018-01-04T00:00:00.000000",
            "operationAmount": {
                "amount": "400.00",
                "currency": {
                    "name": "Russian Ruble",
                    "code": "RUB"
                }
            },
            "description": "Оплата услуг",
            "from": "Карта 3000000000000003",
            "to": "Счет 40000000000000000004"
        }
    ]

@pytest.fixture
def empty_transactions():
    """Fixture for empty list of transactions"""
    return []

@pytest.fixture
def transactions_with_same_currency():
    """Fixture for the only currency cases"""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2018-01-01T00:00:00.000000",
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "name": "US Dollar",
                    "code": "USD"
                }
            },
            "description": "Перевод 1",
            "from": "Счет 1",
            "to": "Счет 2"
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2018-01-02T00:00:00.000000",
            "operationAmount": {
                "amount": "200.00",
                "currency": {
                    "name": "US Dollar",
                    "code": "USD"
                }
            },
            "description": "Перевод 2",
            "from": "Счет 3",
            "to": "Счет 4"
        }
    ]