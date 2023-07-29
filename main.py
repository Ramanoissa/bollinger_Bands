import sqlite3
import pandas as pd
import tele as tb
from symbols import symbols

class TradingStrategy:
    def __init__(self):
        self.connection = sqlite3.connect('price_data.db')

    def calculate_stoploss(self, kaufpreis, current_price, trailing_offset=0.05):
        stoploss = kaufpreis - (kaufpreis * 0.03)
        trailing_stop = kaufpreis + (kaufpreis * trailing_offset)

        if current_price > trailing_stop:
            stoploss = current_price - (current_price * 0.03)

        return stoploss

    async def kaufsignal(self):
        cursor = self.connection.cursor()
        symbols = symbols

        for symbol in symbols:
            query = f"SELECT * FROM price_data WHERE symbol='{symbol}' ORDER BY timestamp DESC LIMIT 1"
            df = pd.read_sql_query(query, self.connection)

            if df.empty:
                continue

            columns_to_convert = ['close', 'bb_upperband', 'bb_middleband', 'bb_lowerband', 'bb_lowerband_value', 'bb_upperband_value', 'bb_percentage_diff']
            df[columns_to_convert] = df[columns_to_convert].apply(pd.to_numeric)

            if df['bb_percentage_diff'].iloc[0] <= 0.04:
                kaufpreis = df['close'].iloc[0] * 1.7 - df['close'].iloc[0]
                current_price = df['close'].iloc[0]
                stoploss = self.calculate_stoploss(kaufpreis, current_price)

                message = f"Kaufsignal für {symbol} - Kaufpreis: {kaufpreis:.2f}, Stoploss: {stoploss:.2f}"
                tb.telegram_send_message(message)

            else:
                message = f"Kein Kaufsignal für {symbol}."
                tb.telegram_send_message(message)

    def close(self):
        self.connection.close()

    async def main(self):
        await self.kaufsignal()

# Erstelle eine Instanz von TradingStrategy und führe die Methode main asynchron aus
if __name__ == "__main__":
    import asyncio
    trading_strategy = TradingStrategy()
    asyncio.run(trading_strategy.main())
    trading_strategy.close()
