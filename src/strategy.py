
def add_rsi_condition(data):
    data["condition_rsi"] = (data["RSI_14"] > 30) & (data["RSI_14"] < 60)
    return data

def add_ema_condition(data):
    data["condition_ema"] = data["Close"] > data["EMA_50"]
    return data

def add_macd_condition(data):
    data["condition_macd"] = data["MACD_12_26_9"] > data["MACDs_12_26_9"]
    return data

def add_vol_condition(data):
    data["condition_vol"] = data["Volume"] > data["SMA_VOLUME"] 
    return data

#Assigning signal 
def assign_signal(data):
    data["Signal"] = None #initialisation de la colonne pour éviter de garder des traitements précédents
    data.loc[data["condition_rsi"] & data["condition_ema"] & data["condition_macd" ] & data["condition_vol"], "Signal"] = "Strong Buy"
    data.loc[(data["Signal"].isna()) & data["condition_rsi"] & data["condition_ema"] & data["condition_macd" ], 'Signal'] = "Buy"
    data.loc[(data["Signal"].isna()), "Signal"] = "Wait"
    return data

#fonction globale 
def run_strategy(data):
    add_rsi_condition(data)
    add_ema_condition(data)
    add_macd_condition(data)
    add_vol_condition(data)
    assign_signal(data)
    return data