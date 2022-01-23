"""API Alerts entry point script."""
# alerts/__main__.py

from cmath import log
import logging, argparse
from alerts import alerts

def main(symbol, debug, logfile):
    """ Main function to kick off the program

    :param: symbol Ticker symbol that should be used for the program
    :param: debug Level for the logger to utilize defaults to info
    :logfile: logfile Location of the logfile to store logs defaults to logfile.log
    
    """
    if debug:
        alerts.set_logger(level=logging.DEBUG,logfile=logfile)
    else:
        alerts.set_logger(level=logging.INFO,logfile=logfile)

    alerts.api_alerts(symbol=symbol)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--symbol',  type=str, help="Ticker symbol tested for price deviation", required=True)
    parser.add_argument('-d', '--debug',   action='store_true', help="Sets log level to debug to track help track down issues")
    parser.add_argument('-l', '--logfile', type=str, help="Name of the logfile to store logs")
    args = parser.parse_args()

    logfile = args.logfile
    debug = args.debug
    symbol = args.symbol

    if not isinstance(debug, bool):
        debug = False

    if not isinstance(logfile, str):
        logfile = "logfile.log"

    main(symbol, debug, logfile)
