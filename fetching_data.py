import yfinance as yf 
import pandas_ta as ta
import pandas as pd

all_data = []  # liste pour stocker les dataframes
stocks = [
    "CA.PA",    # Crédit Agricole
    "GLE.PA",   # Société Générale
    "BNP.PA",   # BNP Paribas
    "AIR.PA",   # Airbus
    "MC.PA",    # LVMH
    "OR.PA",    # L'Oréal
    "SAN.PA",   # Sanofi
    "DG.PA",    # Vinci
    "SU.PA",    # Schneider Electric
    "HO.PA"     # Thales
]

for ticker in stocks: 
    print(f"Data for {ticker}") # this prints the stocks in different lines 
    try:
        stock_data = yf.Ticker(ticker) # this answers to : what do i look for in yahoo ? 
        data = stock_data.history(period="5y", interval = "1wk") #historique d'un an et interval d'une semaine
        data.ta.rsi(length=14, append=True) #calcul RSI sur 14 jours et l'ajoute dans le dataframe -> append = true
        data[['RSI_14']] = data[['RSI_14']].round(2)
        data.ta.macd(append=True) # calcul MACD
        data[['MACD_12_26_9', 'MACDs_12_26_9']] = data[['MACD_12_26_9', 'MACDs_12_26_9']].round(2)
        data['SMA12'] = data.ta.sma(length=12, append=True, close = 'Close').round(2) # Calcul de la Moyenne sur 12 candles
        data.ta.ema(length=50, append=True)#calcul de EMA sur 12
        data[['EMA_50']] = data[['EMA_50']].round(2)
        data['Vol_avg']= data.ta.sma(length=12, append=True, close='Volume') # Add 'volume_avg' to the list. added close because its in default on price, but now we use it for volume. It's case sensitive 
        data['Ticker'] = ticker
        data['ATR_14'] = data.ta.atr(length=14, append=True)
        data_display = data[['Ticker','Open','Close', 'Low','Volume','High','RSI_14','MACD_12_26_9','MACDs_12_26_9','SMA12','EMA_50','Vol_avg','ATR_14']] #affichage des colonnes
        data_display['Signal'] = pd.NA #ajouter la colonne signal vide pour débloquer les conditions dans le data_display (version filtrée) pas dans data 
        data_display['Entry_Price'] = pd.NA 
        data_display['Result'] = pd.NA
        data_display["weeks_to_result"] = pd.NA
        data_display["+/- Value"] = pd.NA
        #data_display["Close_next_week"] = pd.NA
        # print(data.columns) # for displaying headers


        #Conditions sur la vue filtrée et pas la data
        trend_filter = (data_display['Close']> data_display['EMA_50'])
        setup = (data_display['RSI_14'] > 30) & (data_display['RSI_14'] < 65)
        trigger = (data_display['MACD_12_26_9'] > data_display['MACDs_12_26_9'])
        volume_indicator = (data_display['Volume'] > data_display['Vol_avg'])

        #Assign signals 
        data_display.loc[trend_filter & setup & volume_indicator & trigger, 'Signal'] = '✅ Strong Buy' #fonction loc permet de cibler la ligne et rajouter une colonne
        data_display.loc[(data_display['Signal'].isna()) & trend_filter & setup & trigger, 'Signal'] = '✌️ Buy' #SI la condition précedente est NA then regarde celle la
        data_display.loc[data_display['Signal'].isna(), 'Signal'] = '💤 Wait' #SI la condition précedente est NA then regarde celle la

        #Backtesting 

        #data_display.loc[data_display['Signal'].isin(["✅ Strong Buy","✌️ Buy"]), "% de perf"] = ((data_display["Close"].shift(-1) - data_display["Close"]) / data_display["Close"])*100  #créé une colonne close next week si les conditions sont remplies et récupérer le prix close de la semaine suivante 
        #data_display.loc[data_display['% de perf']>0, "Result"] = 'Win'
        #data_display.loc[data_display['% de perf']<=0, "Result"] = 'Loss'

        # Clacul de l'Entry_Price

        #for i in range(len(data_display)-1): 
        #    try:
        #        if data_display.iloc[i]["Signal"] in ["✅ Strong Buy", "✌️ Buy"]:
        #            data_display.iloc[i, data_display.columns.get_loc("Entry_Price")] = data_display.iloc[i+1]["Open"]
        #    except Exception as e :
        #        print(f"⚠️ Problème à la ligne {i} pour {ticker} : {e}")

        #Calcul Take Profit & Stop Loss

        #data_display.loc[data_display['Signal'] == "✅ Strong Buy" , "TP"] = data_display["Entry_Price"] + (5 * data_display["ATR_14"])
        #data_display.loc[data_display['Signal'] == "✌️ Buy" , "TP"] = data_display["Entry_Price"] + (5 * data_display["ATR_14"])

        #data_display.loc[data_display['Signal'] == "✅ Strong Buy", "SL"] = data_display["Entry_Price"] - (2.5 * data_display["ATR_14"])
        #data_display.loc[data_display['Signal'] == "✌️ Buy" , "SL"] = data_display["Entry_Price"] - (2.5 * data_display["ATR_14"])

        #Calcul de Wins/Loss et nombre de semaine


        in_position = False
        i = 0
        while i < len(data_display) - 1:
            if not in_position and data_display.iloc[i]["Signal"] in ["✅ Strong Buy", "✌️ Buy"]:
                idx = data_display.index[i]
                entry_price = data_display.iloc[i + 1]["Open"]
                atr = data_display.iloc[i]["ATR_14"]
                data_display.loc[idx, "Entry_Price"] = entry_price
                data_display.loc[idx, "TP"] = entry_price + (5 * atr)
                data_display.loc[idx, "SL"] = entry_price - (2.5 * atr)
                in_position = True
                

                for j in range(i + 1, len(data_display)):
                    high = data_display.iloc[j]["High"]
                    low = data_display.iloc[j]["Low"]
                    tp = data_display.iloc[i]["TP"]
                    sl = data_display.iloc[i]["SL"]

            
                    # ⚠️ Adversarial assumption: SL hit first if both hit in same week
                    if low <= sl and high >= tp:
                        data_display.loc[idx, "Result"] = "loss"
                        data_display.loc[idx, "weeks_to_result"] = j - i
                        money_result = data_display.loc[idx]["SL"] - entry_price
                        data_display.loc[idx, "+/- Value"] = money_result
                        in_position = False
                        i=j
                        break

                    elif high >= tp:
                        data_display.loc[idx, "Result"] = "win"
                        data_display.loc[idx, "weeks_to_result"] = j - i
                        money_result = data_display.loc[idx]["TP"] - entry_price
                        data_display.loc[idx, "+/- Value"] = money_result
                        in_position = False
                        i=j
                        break

                    elif low <= sl:
                        data_display.loc[idx, "Result"] = "loss"
                        data_display.loc[idx, "weeks_to_result"] = j - i
                        money_result = data_display.loc[idx]["SL"] - entry_price
                        data_display.loc[idx, "+/- Value"] = money_result
                        in_position = False
                        i=j
                        break

                    # Zombie Trades 
                    if j - i == 12: 
                        exit_price = data_display.iloc[j]["Close"]
                        if  exit_price > entry_price:
                            data_display.loc[idx, "Result"] = "win"
                            money_result = exit_price - entry_price
                            data_display.loc[idx, "+/- Value"] = money_result
                        elif exit_price < entry_price:
                            data_display.loc[idx, "Result"] = "loss"
                            money_result = exit_price - entry_price
                            data_display.loc[idx, "+/- Value"] = money_result
                        else: 
                            data_display.loc[idx, "Result"] = "flat"
                        data_display.loc[idx, "weeks_to_result"] = 12
                        in_position = False
                        i=j
                        break

            i += 1

        # ajoute chaque dataframe à la liste
        all_data.append(data_display)  

        #print result
        print(data_display.tail(3)) # tail une fonction pour prendre les 5 dernières lignes (tu peux faire header pour le contraire)
        print() #un espace entre loop 
    except Exception as e:
        print(f"Error with : {ticker} : {e} \nSkipping...\n") #{e} pour afficher l'erreur 

# Une fois la boucle finie, on concatène tout
final_df = pd.concat(all_data, ignore_index=True)

# Calcul indicateurs
count_positions = final_df['Result'].isin(["win","loss"]).sum() #sum() retourne des boolean true or false raison pourlaquelle on fait sum et pas count
count_wins = (final_df['Result'] == 'win').sum()
result_value = final_df["+/- Value"].sum()
print("Nombre de Positions", count_positions)
print("Nombre de wins", count_wins)
print(result_value)
#print("% de perf", perc_perfor)

# Et là tu exportes ton CSV final
final_df.to_csv("resultats_backtest.csv", index=False)
