"""
Tests for generators.py
"""

from typing import Generator

import pytest

from generators import card_number_generator, filter_by_currency, get_transaction_descriptions

'''
Tests for filter_by_currency
'''

# Valid cases
@pytest.mark.parametrize("currency", ["USD", "EUR", "RUB", "BYR"])
def test_filter_by_currency_parametrized(sample_gen_transactions, currency):
    """Parametrised test for different currencies"""
    filtered = list(filter_by_currency(sample_gen_transactions, currency))
    assert all(t["operationAmount"]["currency"]["code"] == currency for t in filtered)


def test_filter_by_currency_case_insensitive(sample_gen_transactions):
    """Tests for case-insensitivity"""
    usd_lower = list(filter_by_currency(sample_gen_transactions, "usd"))
    usd_upper = list(filter_by_currency(sample_gen_transactions, "USD"))
    usd_mixed = list(filter_by_currency(sample_gen_transactions, "UsD"))

    assert usd_lower == usd_upper == usd_mixed
    assert len(usd_lower) == 2


def test_filter_by_currency_multiple_currencies(sample_gen_transactions):
    """Tests for different currencies"""
    eur_transactions = list(filter_by_currency(sample_gen_transactions, "EUR"))
    rub_transactions = list(filter_by_currency(sample_gen_transactions, "RUB"))

    assert len(eur_transactions) == 1
    assert eur_transactions[0]["id"] == 2
    assert eur_transactions[0]["operationAmount"]["currency"]["code"] == "EUR"

    assert len(rub_transactions) == 1
    assert rub_transactions[0]["id"] == 4
    assert rub_transactions[0]["operationAmount"]["currency"]["code"] == "RUB"


def test_filter_by_currency_returns_filter_object(sample_gen_transactions):
    """Test for result type"""
    result = filter_by_currency(sample_gen_transactions, "USD")

    assert isinstance(result, filter)

# Edge cases
def test_filter_by_currency_empty_result(sample_gen_transactions):
    """Inexistent currency test"""
    gbp_transactions = list(filter_by_currency(sample_gen_transactions, "GBP"))

    assert len(gbp_transactions) == 0
    assert gbp_transactions == []


def test_filter_by_currency_valid_case(sample_gen_transactions):
    """The only currency test"""
    usd_filter = filter_by_currency(sample_gen_transactions, "USD")
    usd_transactions = list(usd_filter)

    assert len(usd_transactions) == 2
    assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in usd_transactions)
    assert usd_transactions[0]["id"] == 1
    assert usd_transactions[1]["id"] == 3


def test_filter_by_currency_empty_list(empty_transactions):
    """Empty list test"""
    result = list(filter_by_currency(empty_transactions, "USD"))

    assert len(result) == 0
    assert result == []


def test_filter_by_currency_all_match(transactions_with_same_currency):
    """All transactions match filtration"""
    usd_transactions = list(filter_by_currency(transactions_with_same_currency, "USD"))

    assert len(usd_transactions) == 2
    assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in usd_transactions)


# Invalid cases (raising exception)


def test_filter_by_currency_none_transactions():
    """Test for None instead of list"""
    with pytest.raises(TypeError):
        list(filter_by_currency(None, "USD"))


def test_filter_by_currency_none_currency(sample_gen_transactions):
    """Test for None instead of currency"""
    with pytest.raises(AttributeError):
        list(filter_by_currency(sample_gen_transactions, None))


def test_filter_by_currency_invalid_transactions_structure():
    """Test for incorrect transactions structure"""
    invalid_transactions = [
        {"id": 1, "operationAmount": {"amount": "100.00"}},  # Нет currency
        {"id": 2, "operationAmount": {"currency": {"name": "USD"}}},  # Нет code
    ]

    with pytest.raises(KeyError):
        list(filter_by_currency(invalid_transactions, "USD"))


'''
Tests for get_transaction_descriptions
'''

# Valid cases


def test_transaction_descriptions_valid_case(sample_gen_transactions):
    descriptions = list(get_transaction_descriptions(sample_gen_transactions))

    expected_descriptions = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Оплата услуг"
    ]

    assert descriptions == expected_descriptions
    assert len(descriptions) == len(sample_gen_transactions)


def test_transaction_descriptions_returns_generator(sample_gen_transactions):
    """Test for result type"""
    result = get_transaction_descriptions(sample_gen_transactions)

    assert isinstance(result, Generator)


# Edge cases


def test_transaction_descriptions_empty_list(empty_transactions):
    """Test for an empty list"""
    descriptions = list(get_transaction_descriptions(empty_transactions))

    assert len(descriptions) == 0
    assert descriptions == []


def test_transaction_descriptions_lazy_evaluation(sample_gen_transactions):
    """Lazy counting test"""
    generator = get_transaction_descriptions(sample_gen_transactions)

    # Берем только первые два описания
    first = next(generator)
    second = next(generator)
    third = next(generator)
    fourth = next(generator)

    assert first == "Перевод организации"
    assert second == "Перевод со счета на счет"
    assert third == "Перевод с карты на карту"
    assert fourth == "Оплата услуг"


def test_transaction_descriptions_duplicate_descriptions():
    """Test for same descriptions in different transactions"""
    transactions = [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2018-01-01T00:00:00.000000",
            "operationAmount": {
                "amount": "100.00",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Перевод организации",
            "from": "Счет 1",
            "to": "Счет 2"
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2018-01-02T00:00:00.000000",
            "operationAmount": {
                "amount": "200.00",
                "currency": {"name": "EUR", "code": "EUR"}
            },
            "description": "Перевод организации",  # Такое же описание
            "from": "Счет 3",
            "to": "Счет 4"
        }
    ]

    descriptions = list(get_transaction_descriptions(transactions))

    assert descriptions == ["Перевод организации", "Перевод организации"]
    assert len(descriptions) == 2


# Invalid tests (raising exception)


def test_transaction_descriptions_none_transactions():
    """Test for None instead of list"""
    with pytest.raises(TypeError):
        list(get_transaction_descriptions(None))


def test_transaction_descriptions_invalid_structure():
    """Test for invalid transactions structure"""
    invalid_transactions = [
        {"id": 1},  # Нет description
        {"description": "Test"},  # Неполная структура
    ]

    with pytest.raises(KeyError):
        list(get_transaction_descriptions(invalid_transactions))


def test_transaction_descriptions_missing_description():
    """Test for missing description key"""
    transactions = [
        {
            "id": 1,
            "state": "EXECUTED",
            "description": "Перевод организации"
        },
        {
            "id": 2,
            "state": "EXECUTED"
            # Нет description
        }
    ]

    generator = get_transaction_descriptions(transactions)

    assert next(generator) == "Перевод организации"

    with pytest.raises(KeyError):
        next(generator)


'''
Tests for card_number_generator
'''

# Valid cases tests


def test_generator_returns_correct_format():
    generator = card_number_generator(1, 5)

    results = list(generator)
    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005"
    ]

    assert results == expected
    assert all(len(item) == 19 for item in results)  # XXXX XXXX XXXX XXXX = 16 digits + 3 spaces
    assert all(item.count(' ') == 3 for item in results)


def test_generator_is_generator():
    """Test for generator object as an output"""
    result = card_number_generator(1, 10)
    assert isinstance(result, Generator)


# Edge cases tests


@pytest.mark.parametrize("start,stop,expected_first,expected_last", [
    (1, 3, "0000 0000 0000 0001", "0000 0000 0000 0003"),
    (9999, 10001, "0000 0000 0000 9999", "0000 0000 0001 0001"),
    (1234123412341234, 1234123412341236, "1234 1234 1234 1234", "1234 1234 1234 1236"),
])
def test_generator_first_last_values(start, stop, expected_first, expected_last):
    """First and last items in sequence expected to be"""
    generator = card_number_generator(start, stop)
    results = list(generator)

    assert results[0] == expected_first
    assert results[-1] == expected_last


@pytest.mark.parametrize("start,stop,expected_count", [
    (1, 1, 1),
    (1, 10, 10),
    (9999999999999990, 9999999999999999, 10),
    (1000, 1005, 6),
])
def test_generator_range_length(start, stop, expected_count):
    """Test for expected length of the sequence"""
    generator = card_number_generator(start, stop)
    results = list(generator)

    assert len(results) == expected_count


# Tests for exceptions catching


def test_empty_arguments():
    """Test for empty arguments"""
    with pytest.raises(ValueError, match="Not all arguments have been given"):
        list(card_number_generator(None, 10))

    with pytest.raises(ValueError, match="Not all arguments have been given"):
        list(card_number_generator(1, None))


def test_non_integer_arguments():
    """Tests for non-integer arguments"""
    with pytest.raises(ValueError, match="Invalid input: Arguments must be integers"):
        list(card_number_generator("1", 10))

    with pytest.raises(ValueError, match="Invalid input: Arguments must be integers"):
        list(card_number_generator(1, "10"))

    with pytest.raises(ValueError, match="Invalid input: Arguments must be integers"):
        list(card_number_generator(1.5, 10))


def test_invalid_range():
    """Tests for invalid ranges"""
    with pytest.raises(ValueError, match="Not all arguments have been given or '0' given as an argument"):
        list(card_number_generator(0, 10))

    with pytest.raises(ValueError, match="Arguments must be between 1 and 9999999999999999"):
        list(card_number_generator(1, 10000000000000000))

    with pytest.raises(ValueError, match="Arguments must be between 1 and 9999999999999999"):
        list(card_number_generator(-5, 10))


def test_start_greater_than_stop():
    """Test for stop > start"""
    with pytest.raises(ValueError, match="Arguments must be between 1 and 9999999999999999"):
        list(card_number_generator(10, 5))
