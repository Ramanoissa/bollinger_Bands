import get_data
from bollinger import df
from symbols import symbols
import numpy as np
import pandas as pd
from calculate_percentage_difference import calculate_percentage_difference
import tele as tb 
from binanceapi import client 

nachrichten= []
interval=client.KLINE_INTERVAL_1DAY
# Get the initial set of data
get_data.get_prices()

for symbol in symbols:
    # Get data from API
    df['bb_lowerband_value'] = df.apply(lambda row: row['close'] if row.name is None else row.iloc[4], axis=1)
    df['bb_upperband_value'] = df.apply(lambda row: row['close'] if row.name is None else row.iloc[3], axis=1)
    percentage_diff = calculate_percentage_difference(df, symbol)  # Calculate percentage difference
    print("Bollinger Bands for", symbol)
    print("Percentage Difference for", symbol, ":", percentage_diff)

    if percentage_diff <= 0.04 :
        message = f'{symbol}\n  {interval} buysignal'
        print (message)
        if message not in nachrichten :
            tb.telegram_send_message(message)
            nachrichten.append(message)
    else:
        continue
