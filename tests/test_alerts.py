# tests/test_alerts.py

from alerts import alerts
import pytest

TEST_DATA = [1, 2, 3, 4, 5]
TEST_DATA_2 = [1.23, 3.45, 6.54, 10.2]
TEST_STR_DATA = ["1", "2", "3", "4", "5"]
TEST_STR_DATA_2 = ["1.23", "3.45", "6.54", "10.2"]
TEST_FLOAT_DATA = [1.0, 2.0, 3.0, 4.0, 5.0]

def test_calculate_mean():
    assert alerts.calculate_mean(TEST_DATA) == 3
    assert round(alerts.calculate_mean(TEST_DATA_2), 3) == 5.355

def test_calculate_stdev():
    assert round(alerts.calculate_stdev(TEST_DATA), 3) == 1.581
    assert round(alerts.calculate_stdev(TEST_DATA_2), 3) == 3.895

def test_symbols_exists():
    assert alerts.symbols_exists("btcusd")
    assert not alerts.symbols_exists("usd")

    # wrap exception with Pytest to accurately test the issue
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        alerts.symbols_exists("us2")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 'Ticker symbol provided should not have numbers in it'

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        alerts.symbols_exists(123)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 'Ticker symbol provided is not a string'
   
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        alerts.symbols_exists([123])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 'Ticker symbol provided is not a string'


def test_cast_list():
    assert alerts.cast_list(float, TEST_STR_DATA) == TEST_FLOAT_DATA # tests string to float conversion
    assert alerts.cast_list(float, TEST_STR_DATA_2) == TEST_DATA_2 # test strings with decimals to float conversion
    assert alerts.cast_list(int, TEST_STR_DATA) == TEST_DATA # test string to int conversion
    assert alerts.cast_list(str, TEST_DATA_2) == TEST_STR_DATA_2 # test float to string conversion
    assert alerts.cast_list(str, TEST_DATA) == TEST_STR_DATA # test int to string conversion

def test_cast_list_float():
    assert alerts.cast_list_float(TEST_DATA) == TEST_FLOAT_DATA
    assert alerts.cast_list_float(TEST_DATA_2) == TEST_DATA_2

def test_cast_list_string():
    assert alerts.cast_list_string(TEST_DATA) == TEST_STR_DATA
    assert alerts.cast_list_string(TEST_DATA_2) == TEST_STR_DATA_2
