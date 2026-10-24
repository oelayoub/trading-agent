
def run_backtest(data):

    in_position = False
    idx = None
    entry_price = None
    signal_i = None
    i = 0

    while i < len(data) - 1:
        if not in_position and data.iloc[i]["Signal"] in ["Strong Buy", "Buy"]:
            idx = data.index[i]
            signal_i = i
            entry_price = data.iloc[i + 1]["Open"]
            data.loc[idx, "Entry_price"] = entry_price
            atr = data.iloc[i]["ATRr_14"]
            tp = entry_price + (5 * atr)
            sl = entry_price - (2.5 * atr)
            data.loc[idx, "TP"] = tp
            data.loc[idx, "SL"] = sl
            in_position = True

            for j in range(i + 1, len(data)):
                high = data.iloc[j]["High"]
                low = data.iloc[j]["Low"]
                if high >= tp and low <= sl:
                    data.loc[idx, "result"] = "loss"
                    data.loc[idx, "week_to_result"] = j - i
                    data.loc[idx, "profit_loss"] = (sl - entry_price) / entry_price
                    in_position = False
                    i = j
                    break
                elif high >= tp:
                    data.loc[idx, "result"] = "win"
                    data.loc[idx, "week_to_result"] = j - i
                    data.loc[idx, "profit_loss"] = (tp - entry_price) / entry_price
                    in_position = False
                    i = j
                    break
                elif low <= sl:
                    data.loc[idx, "result"] = "loss"
                    data.loc[idx, "week_to_result"] = j - i
                    data.loc[idx, "profit_loss"] = (sl - entry_price) / entry_price
                    in_position = False
                    i = j
                    break
                elif j - i == 12:
                    exit_trade = data.iloc[j]["Close"]
                    data.loc[idx, "week_to_result"] = 12
                    data.loc[idx, "profit_loss"] = (exit_trade - entry_price) / entry_price
                    if exit_trade > entry_price:
                        data.loc[idx, "result"] = "win"
                    elif exit_trade < entry_price:
                        data.loc[idx, "result"] = "loss"
                    else:
                        data.loc[idx, "result"] = "flat"
                    in_position = False
                    i = j
                    break

        i += 1

    # History for this ticker is over: close any trade still open
    if in_position:
        last_j = len(data) - 1
        exit_trade = data.iloc[last_j]["Close"]
        data.loc[idx, "week_to_result"] = last_j - signal_i
        data.loc[idx, "profit_loss"] = (exit_trade - entry_price) / entry_price
        if exit_trade > entry_price:
            data.loc[idx, "result"] = "win"
        elif exit_trade < entry_price:
            data.loc[idx, "result"] = "loss"
        else:
            data.loc[idx, "result"] = "flat"
        in_position = False

    return data
