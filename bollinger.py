import pandas as pd
import numpy as np
from ta.volatility import BollingerBands
import get_data

# Generate random data for demonstration
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', periods=100)
close_prices = np.random.uniform(low=100, high=200, size=(100,))

# Create a DataFrame with explicit dtypes and meaningful column names
df = pd.DataFrame({'date': dates, 'close': close_prices}, dtype=np.float64)

# Initialize the Bollinger Bands indicator
indicator_bb = BollingerBands(close=df['close'], window=20, window_dev=2)

# Compute the upper, middle, and lower bands
df['bb_upperband'] = indicator_bb.bollinger_hband()
df['bb_middleband'] = indicator_bb.bollinger_mavg()
df['bb_lowerband'] = indicator_bb.bollinger_lband()

# Access the specific price values for each row
df['bb_lowerband_value'] = df.apply(lambda row: row['close'] if row.name is None else row.iloc[4], axis=1)
df['bb_upperband_value'] = df.apply(lambda row: row['close'] if row.name is None else row.iloc[3], axis=1)

# Print the DataFrame with Bollinger Bands and the specific price values
print(df)
