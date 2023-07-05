from binanceapi import client
import pandas as pd
import schedule
import time
from symbols import symbols

# Dictionary to store the price data
data = {}

try:
    for symbol in symbols:
        klines = client.get_klines(symbol=symbol, interval=client.KLINE_INTERVAL_1DAY, limit=100)
        if len(klines[0]) != 12:
            print(f"Unexpected number of columns for symbol {symbol}:")
            print(klines)
            continue
        df = pd.DataFrame(
            klines,
            columns=[
                'open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                'taker_buy_quote_asset_volume', 'ignore'
            ]
        )
        df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
        df.set_index('open_time', inplace=True)
        # Store the data in the dictionary
        data[symbol] = df[['open', 'high', 'low', 'close', 'volume']]
    print(data)  # Print the populated data dictionary

except Exception as e:
    print("An error occurred while retrieving price data:", e)



