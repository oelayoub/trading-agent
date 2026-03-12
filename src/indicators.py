from config import RSI_LENGTH
from config import CLOSE_SMA_LENGTH
from config import EMA_LENGTH 
from config import VOLUME_SMA_LENGTH 
from config import ATR_LENGTH
import pandas_ta as ta


def add_rsi(data):
    data.ta.rsi(length = RSI_LENGTH, append=True)
    data["RSI_14"] = data["RSI_14"].round(2)
    return data

def add_close_sma(data):
    data["SMA_CLOSE_12"] = data.ta.sma(length = CLOSE_SMA_LENGTH, close = 'Close')
    return data

def add_ema(data):
    data.ta.ema(length = EMA_LENGTH, append=True)
    data["EMA_50"] = data["EMA_50"].round(2)
    return data

def add_macd(data):
    data.ta.macd(append=True)
    data[['MACD_12_26_9', 'MACDs_12_26_9']] = data[['MACD_12_26_9', 'MACDs_12_26_9']].round(2)
    return data

def add_volume_avg(data):
    data["SMA_VOLUME"] = data.ta.sma(length = VOLUME_SMA_LENGTH, close = 'Volume')
    return data

def add_atr(data):
    data.ta.atr(length = ATR_LENGTH, append=True)
    data["ATRr_14"] = data["ATRr_14"].round(2)
    return data

def calculate_indicators(data):
    data = add_rsi(data)
    data = add_close_sma(data)
    data = add_ema(data)
    data = add_macd(data)
    data = add_volume_avg(data)
    data = add_atr(data)
    return data