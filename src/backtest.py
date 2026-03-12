
def run_backtest(data):

    in_position = False
    i = 0 

    while i < len(data) - 1:
        if not in_position and data.iloc[i]["Signal"] in ["Strong Buy" , "Buy"]:
            idx = data.index[i] # renvoi le contenu de la série "idx = 2021-01-10"
            entry_price = data.iloc[i+1]["Open"] #calcul de l'entry price 
            data.loc[idx, "Entry_price"] = entry_price # enregistre l'entry price dans sa colonne 
            atr = data.iloc[i]["ATRr_14"] # pour calcul iloc
            tp = entry_price + (5 * atr)
            sl = entry_price - (2.5 * atr) 
            data.loc[idx, "TP"] = tp #pour enregistrer loc 
            data.loc[idx, "SL"] = sl#pour enregistrer loc 
            in_position = True

            for j in range(i+1, len(data)):
                high = data.iloc[j]["High"]
                low = data.iloc[j]["Low"]
                if high>=tp and low<=sl:  # Adversarial assumption: SL hit first if both hit in same week
                    data.loc[idx, "result"] = "loss"
                    data.loc[idx, "week_to_result"] = j - i
                    loss = sl - entry_price
                    data.loc[idx, "profit_loss"] = loss
                    in_position = False
                    i=j
                    break                    
                elif high >= tp: 
                    data.loc[idx, "result"] = "win"
                    data.loc[idx, "week_to_result"] = j - i
                    profit = tp - entry_price
                    data.loc[idx, "profit_loss"] = profit
                    in_position = False
                    i=j
                    break
                elif low <= sl:
                    data.loc[idx, "result"] = "loss"
                    data.loc[idx, "week_to_result"] = j - i
                    loss = sl - entry_price
                    data.loc[idx, "profit_loss"] = loss
                    in_position = False
                    i=j
                    break
                elif j - i == 12:
                    exit_trade = data.iloc[j]["Close"]
                    exit_result = exit_trade - entry_price
                    data.loc[idx, "week_to_result"] = 12
                    if exit_trade > entry_price:
                        data.loc[idx, "result"] = "win"
                    elif exit_trade < entry_price:
                        data.loc[idx, "result"] = "loss"
                    data.loc[idx, "profit_loss"] = exit_result
                    in_position = False
                    i=j
                    break
        i += 1

    return(data)
                