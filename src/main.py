import pandas as pd
from data import load_data
from config import stocks
from indicators import calculate_indicators
from strategy import run_strategy
from backtest import run_backtest
from metrics import calculate_metrics

all_data = []

for ticker in stocks:

    try:

        print(f"Data for {ticker}")

        data = load_data(ticker)

        data = calculate_indicators(data)

        data = run_strategy(data)

        data = run_backtest(data)

        all_data.append(data)

        print(data.tail(3))

    except Exception as e:
        print(f"Error with {ticker}: {e}")

final_data = pd.concat(all_data, ignore_index=True)

metrics = calculate_metrics(final_data)

final_data.to_csv("backtest1403.csv", index=False)

print(metrics)