

# Trading Agent 

## Description : 
This is a python-based trading backtest engine. 
It loads historical data from yahoo finance, calculates technical indicators, generates signals, simulates trades, computes performance metrics, and exports results to a CSV file.

## Features : 
The robot loads data from yahoo finance and calculates technical indicators : 
    - RSI
    - SMA
    - EMA
    - MACD
    - Average Volume
    - ATR

Signals are generated based on a combination of technical conditions.
Backtesting module simulates trades per ticker based on a ratio and a max holding duration ;
Metrics are calculated based on the backtest results to give a performance review ;
The results are exported in a csv file

## Project Structure : 

Project structure : 
trading-agent
    src
        config.py : contains parameters and list of tickers 
        data.py : loads data from yahoo finance 
        indicators.py : calculate technical indicators 
        strategy.py : generates signals based on conditions 
        backtest.py : simulate trades per ticker 
        main.py : orchestrate modules, handles loop and errors, print metrics and export csv file 
    test
        csv file : dataframe for testing
        test_metrics.py : testing metrics 
    

## Strategy : 

Robot generates three types of signals : 
    Strong Buy : all conditions are met 
    Buy : 3 out of 4 conditions are met 
    Wait : Else 

A position is open when a signal is Strong Buy or Buy for a ticker. The entry price for the position corresponds to the opening price of the next week. 

A position is closed when :
    the High is >= Take Profit : entry_price + (5 * atr)
    the Low is <= Stop Loss : entry_price - (2.5 * atr)
    if the trade is open for 12 weeks, the position is closed. The entry price is compared to the closing of the week 12 to determine the results 

if during the same week the high is >= TP and the low is <= SL, the robot considers that the trade is lost 

## Metrics : 
    - Number of positions
    - Number of wins
    - Number of losses
    - Wins ratio
    - Avergae week for wins
    - Average week for losses 
    - Total gain in value 
    - Total loss in value 
    - Profit Factor 

# Limitation :

- Backtesting is run only per ticker and not across the global portfolio
- Signals are backtested independently for each ticker before results are aggregated.
- Transaction costs are not included 
- Strategy is for educational purposes only 

## How to Run

1. Clone the repository

2. Install the required libraries:

pip install pandas yfinance pandas-ta

3. Open `src/config.py` and define:
- the list of tickers
- the strategy parameters

4. Run the main script:

python src/main.py

5. The program will:
- load historical data
- calculate indicators
- generate signals
- run the backtest
- compute metrics
- export the final results to a CSV file