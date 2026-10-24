import pandas as pd

def calculate_metrics(data):

    count_positions = data["Signal"].isin(["Strong Buy", "Buy"]).sum()

    count_trades = data["result"].isin(["win", "loss", "flat"]).sum()

    count_wins = (data["result"] == "win").sum()

    count_loss = (data["result"] == "loss").sum()

    count_flat = (data["result"] == "flat").sum()

    if count_wins == 0:
        ratio_wins = 0
    else: 
        ratio_wins = (count_wins / (count_wins+count_loss)).round(2)

    if not count_wins:
        average_week_win = 0
    else:
        average_week_win = data.loc[data["result"] == "win", "week_to_result"].mean()

    if not count_loss:
        average_week_loss = 0
    else:
        average_week_loss = data.loc[data["result"] == "loss", "week_to_result"].mean()

    total_gain_perc = (data.loc[data["result"] == "win", "profit_loss"].sum()).round(2)

    total_loss_perc = (data.loc[data["result"] == "loss", "profit_loss"].sum()).round(2)

    if total_loss_perc == 0:
        profit_factor = None
    else:

        profit_factor = total_gain_perc / abs(total_loss_perc)

    return{
        "Number of positions" : (count_positions),
        "Number of trades" : (count_trades),
        "Number of wins" : (count_wins),
        "Number of losses" : (count_loss),
        "Number of flat" : (count_flat),
        "Wins ratio" : round(float(ratio_wins),2),
        "Average week for wins" : (average_week_win),
        "Average week for losses" : (average_week_loss),
        "Total gain in %" : (total_gain_perc),
        "Total loss in %" : (total_loss_perc),
        "Profit Factor" : None if profit_factor is None else round(float(profit_factor),2)
    }


    