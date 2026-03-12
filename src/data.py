from config import PERIOD
from config import INTERVAL
import yfinance as yf


def load_data(ticker):
    data = yf.Ticker(ticker).history(period=PERIOD, interval= INTERVAL)
    data["Ticker"] = ticker
    data = data[['Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']]
    return data


