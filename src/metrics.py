import pandas as pd

def calculate_metrics(data):

    count_positions = data["Signal"].isin(["Strong Buy", "Buy"]).sum()

    count_wins = (data["result"] == "win").sum()

    count_loss = (data["result"] == "loss").sum()

    ratio_wins = (count_wins / (count_wins+count_loss)).round(2)

    average_week_win = data.loc[data["result"] == "win", "week_to_result"].mean()

    average_week_loss = data.loc[data["result"] == "loss", "week_to_result"].mean()

    total_gain_value = (data.loc[data["result"] == "win", "profit_loss"].sum()).round(2)

    total_loss_value = (data.loc[data["result"] == "loss", "profit_loss"].sum()).round(2)

    profit_factor = total_gain_value / abs(total_loss_value)

    return{
        "Number of positions" : int(count_positions),
        "Number of wins" : int(count_wins),
        "Number of losses" : int(count_loss),
        "Wins ratio" : round(float(ratio_wins),2),
        "Avergae week for wins" : int(average_week_win),
        "Average week for losses" : int(average_week_loss),
        "Total gain in value" : int(total_gain_value),
        "Total loss in value" : int(total_loss_value),
        "Profit Factor" : round(float(profit_factor),2)
    }


    