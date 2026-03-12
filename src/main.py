from data import load_data
from indicators import calculate_indicators
from strategy import run_strategy
from backtest import run_backtest

ticker = "CA.PA"

data = load_data(ticker)

data = calculate_indicators(data)

data = run_strategy(data)

data = run_backtest(data)

data.to_csv("backtest1203.csv", index=False)
print(data.tail(3))