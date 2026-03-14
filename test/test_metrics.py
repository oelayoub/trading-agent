
import pandas as pd

df = pd.read_csv("backtest1203.csv")

count_positions = df["Signal"].isin(["Strong Buy", "Buy"]).sum()

count_wins = (df["result"] == "win").sum()

count_loss = (df["result"] == "loss").sum()

ratio_wins = ((count_wins / count_positions) * 100).round(2)

average_week_win = df.loc[df["result"] == "win", "week_to_result"].mean()

average_week_loss = df.loc[df["result"] == "loss", "week_to_result"].mean()

total_gain_value = (df.loc[df["result"] == "win", "profit_loss"].sum()).round(2)

total_loss_value = (df.loc[df["result"] == "loss", "profit_loss"].sum()).round(2)

profit_factor = (total_gain_value / abs(total_loss_value)).round(2)


print(f"Number of positions {count_positions}")
print(f"Number of wins {count_wins}, Number of losses {count_loss}, wins percentage {ratio_wins}%")
print(f"Average number of weeks for wins {average_week_win}")
print(f"Average number of weeks for losses {average_week_loss}")
print(f"Total gains {total_gain_value} euros")
print(f"Total losses {total_loss_value} euros")
print(profit_factor)







