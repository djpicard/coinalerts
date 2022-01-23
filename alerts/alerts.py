# alerts/alerts.py

import json, statistics, datetime, logging, sys
from urllib.error import HTTPError
from xmlrpc.client import Boolean # builtin modules

import requests
from urllib3 import Timeout # extra modules

###
# Constants
###
BASE_URL_V1 = "https://api.gemini.com/v1"
BASE_URL_V2 = "https://api.gemini.com/v2"
LOGGER = logging.getLogger()
SYMBOLS_LIST = []

def cast_list(func, data): 
    """ Cast list

    :param: func Function that will be enacted against every element in the list
    :param: data List to be converted
    :return: list List of all element that have been cast into a new type

    Function that takes a list and a function to convert every element in the list using the function
    """

    LOGGER.debug(f"Func: cast_list, List: {data}")

    return list(map(func, data))


def cast_list_float(data): 
    """ Cast list

    :param: data List to be converted
    :return: list Converted list where elementes were converted to floats

    Function that takes a list and a function to convert every element in the list using the function
    """

    LOGGER.debug(f"Func: cast_list_float, List: {data}")

    return cast_list(float, data)


def cast_list_string(data): 
    """ Cast list

    :param: list List to be converted
    :return: list Converted list where elementes were converted to strings

    Function that takes a list and a function to convert every element in the list using the function
    """

    LOGGER.debug(f"Func: cast_list_string, List: {data}")

    return cast_list(str, data)


def get_list_of_symbols():
    """ Call and get a list of all supported symbols
    
    :return: json Json of the symbols that are supported
    """
    try:
        response = requests.get(f"{BASE_URL_V1}/symbols")
        LOGGER.debug(f"get_list_of_symbols Response: {response}")
        return response.json()
    except requests.exceptions.RequestException as e:
        LOGGER.error(e)
        raise SystemExit(e)


def symbols_exists(symbol):
    """ Check to ensure that the symbole is available

    :param: symbol String of the symbol to run the program against
    """

    LOGGER.debug(f"Func: symbols_exists, Symbol: {symbol}")

    # Ensure that the symbol is a valid string
    if not isinstance(symbol, str):
        msg = "Ticker symbol provided is not a string"
        LOGGER.error(msg)
        raise SystemExit(msg)

    # Symbol should not contain any numbers
    # any will return true if any value in the list is true
    # applying str.isdigit to each char in symbol
    # this is done with the map function and converted to a list of results
    if any(list(map(str.isdigit, symbol))):
        msg = "Ticker symbol provided should not have numbers in it"
        LOGGER.error(msg)
        raise SystemExit(msg)

    # Not testing string length as that will vary depending on ticker pair
    # Return if the symbol is present in the symbols list
    return get_list_of_symbols().count(symbol) > 0


def calculate_stdev(day_changes):
    """ Returns the stdev of the list of values

    :param: day_changes List of changes in price in floats

    :return: float The statistical standard deviation of the list
    """

    LOGGER.debug(f"Func: calculate_stdev, 24hr Changes: {day_changes}")

    return statistics.stdev(day_changes)


def calculate_mean(day_changes):
    """ Returns the mean of the list of values

    :param: day_changes List of changes in price in floats

    :return: float The statistical mean of the list
    """

    LOGGER.debug(f"Func: calculate_mean, 24hr Changes: {day_changes}")

    return statistics.mean(day_changes)


def calc_percent_change(current, average):
    """ Calculates the percent change of two values
    
    :param: current New value to test against, must be a number
    :param: average Current value to test against, must be a number

    :return: float Percentage change between both numbers
    """
    if current == average:
        return 100.0
    try:
        return abs((current - average) / average) * 100
    except ZeroDivisionError:
        return 0


def price_deviation(current_price, day_changes):
    """ Returns results for a price deviation

    :param: current_price Current price of the symbol
    :param: day_changes List of price fluxuations from the last 24hrs

    :return: bool Returns a bool if the price deviates more than a stdev
    """

    LOGGER.debug(f"Func: price_deviation, Current Price: {current_price}, 24hr Changes: {day_changes}")

    # need to convert strings to floats for calculations
    day_changes_float = cast_list_float(day_changes)
    current_price_float = float(current_price)
    stdev = calculate_stdev(day_changes_float)
    average = calculate_mean(day_changes_float)
    change = abs(current_price_float - average)
    percent = round(calc_percent_change(current_price_float, average), 2)

    if change > stdev:
        LOGGER.debug(f"Func: price_deviation: Deviation was greater than stdev")
        return True, round(average, 2), round(change, 2), percent
    LOGGER.debug(f"Func: price_deviation: Deviation was not greater than stdev")
    return False, round(average, 2), round(change, 2), percent

def gather_ticker_data(symbol) -> json:
    """ Call and get ticker information from the Ticker V2 implementation
    
    :return: json Json data related to the ticket. Reference: https://docs.gemini.com/rest-api/#ticker-v2
    """
    try:
        response = requests.get(f"{BASE_URL_V2}/ticker/{symbol}")
        LOGGER.debug(f"Func: gather_ticket_data, Symbol: {symbol}, Response: {response}")
        return response.json()
    except requests.exceptions.RequestException as e:
        LOGGER.error(e)
        raise SystemExit(e)


def send_alert(deviated, average, change, percent, symbol, current_price):
    """ Formats alert into desired output

    :param: deviated Bool to determine if the price has changed by a stdev from average
    :param: average The calculated average of the last 24hrs
    :param: change The nominal value of the change
    :param: percent The percentage of change
    :param: symbol Ticker symbol that is being searched
    :param: current_price Current price of the ticker that is being searched

    :return: json A json representation of the output for the alert to be sent
    """

    # TODO: implement level to show what log level is currently in place
    # TODO: Unit tests for this function
    alert = {
        "timestamp": f"{datetime.datetime.now().isoformat()}", # get timestamp in ISO8601 format
        "level": "INFO",
        "trading_pair": f"{symbol}",
        "deviation": f"{deviated}",
        "data": {
            "last_price": f"{current_price}",
            "average": f"{average}",
            "change": f"{change}",
            "sdev": f"{percent}"
        }
    }

    return json.dumps(alert, indent=4)
    


def api_alerts(symbol) -> None:
    """ Function that determines if a symbol has gone over a single deviation of change from the average

    :param: symbol Ticker symbol that is tested against

    This function will not return a value but will have an alert send to stdout in the event 
    that the price has changed by a stdev from the average price.
    """

    # TODO: Setup price deviation more or less than 1 deviation
    # TODO: Setup default value to fun all ticker symbols

    LOGGER.debug(f"Func: api_alerts, Symbol: {symbol}")
    
    # test Ticker symbol for validity
    exists = symbols_exists(symbol)
    LOGGER.debug(f"Func: api_alerts, Symbol {symbol} is present in list of tickers: {exists}")
    
    # get json for the day's results
    data = gather_ticker_data(symbol)
    LOGGER.debug(f"Func: api_alerts, Data gathered for the symbol {symbol}: {data}")

    if "result" in data:
        LOGGER.error(data["message"])
        raise SystemExit(data["message"])

    # calculate price deviation
    deviated, average, change, percent = price_deviation(data["close"], data["changes"])
    LOGGER.debug(f"Func: api_alerts, Deviated: {deviated}, Average: {average}, Change: {change}, Percent: {percent}")

    # set alert if needed
    #if deviated:
    print(send_alert(deviated, average, change, percent, symbol, data["close"]))

def set_logger(level=logging.INFO, logfile="logfile.log"):
    """ Set the parameters for the logging of the application

    :param: level Logging level to use, defaults to INFO
    :param: logfile Log file location where logs should be stored
    
    """
    log_format = "%(levelname)s %(asctime)s - %(message)s"
    LOGGER.setLevel(level)
    file_handler = logging.FileHandler(logfile)
    formatter = logging.Formatter(log_format)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    LOGGER.addHandler(stdout_handler)
    LOGGER.addHandler(file_handler)
