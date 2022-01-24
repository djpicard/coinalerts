# Introduction

This repo is my submission for teh Gemini take home coding challenge.

## Problem Statement
Price Deviation - Generate an alert if the current price is more than one standard deviation from the 24hr average

## Approach to solving problem
- Understand the problem and research API
- Identify key API functions that will need to be called
- Identify key calculations that will need to be created
- write out function names of potentially needed function with a body of just pass to start
- identify if funtions are composable and could be useful if made as generic as possible
- Write func descriptions
- Start combining functions to build out solution
- Write test cases functions are made to ensure solution outputs desired results
- Cleanup functions and focus on user interactions 

## Time Taken
Total time:   4 hours
Start time:   11:00pm 1/22/22
Break time:   12:00am 1/23/22
Break end:    12:26am 1/23/22
Finish time:  03:32am 1/23/22

# Installation
## Python Version
Python Version 3.8.10

## Pip Installation
pip install -r requirements.txt

## Python run command
python3 -m alerts 

## Options
-h Help Menu
-d Set debug mode for debug output
-s <Symbol> Sets the symbol to search search for alerts

# TODO
## Improvements
- Expand tests in pytest
- Fix symbol check to be more encompassing of different errors
- Review functions and streamline them to be maintainable
- Review functions and reduce globals usage
- Better logging and log levels

## Feature Enhancements
- If symbol are not provided then search all symbols
- Allow ability to set number of stdev to alert on, not just 1 stdev
- RSI or MACD indicators to look for other indicators with more history
