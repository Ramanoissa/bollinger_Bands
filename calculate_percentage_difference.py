from symbols import symbols 
from bollinger import df


def calculate_percentage_difference(df, symbol):
    symbol_data = df[df['symbol'] == symbol]  # Filter data for the given symbol
    upper = symbol_data['upper'].values[0]
    lower = symbol_data['lower'].values[0]

    # Calculate percentage difference
    percentage_diff = (upper - lower) / lower * 100

    return percentage_diff
# Assuming you have the DataFrame df with the required columns (including 'symbol', 'upper', and 'lower')
# Calculate overall percentage difference for all symbols
percentage_difference = 0
for symbol in df['symbol'].unique():
    percentage_diff = calculate_percentage_difference(df, symbol)
    percentage_difference += percentage_diff

print("Overall Percentage Difference:", percentage_difference)



# Calculate percentage difference for a specific symbol
percentage_diff = calculate_percentage_difference(df, symbol)
print("Percentage Difference for", symbol, ":", percentage_diff)
