import get_data
from bollinger import df
from symbols import symbols
import numpy as np
import pandas as pd
from calculate_percentage_difference import calculate_percentage_difference

for symbol in symbols:
    # Get data from API
    get_data
    df['bb_lowerband_value'] = df.apply(lambda row: row['close'] if row.name is None else row.iloc[4], axis=1)
    df['bb_upperband_value'] = df.apply(lambda row: row['close'] if row.name is None else row.iloc[3], axis=1)
    percentage_diff = calculate_percentage_difference(df, symbol)  # Calculate percentage difference
    print("Bollinger Bands for", symbol)
    print("Percentage Difference for", symbol, ":", percentage_diff)
