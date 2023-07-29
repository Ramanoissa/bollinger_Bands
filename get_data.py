import pandas as pd
import logging
import sqlite3
from datetime import datetime, timedelta
from ta.volatility import BollingerBands
from binance.websockets import BinanceSocketManager
from binanceapi import pkey, skey, Client
import threading
from dateutil import parser
from symbols import symbols


# Initialize logger
logging.basicConfig(filename='data_loader_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PriceDataRetriever:
    def __init__(self):
        self.data = {}  # Dictionary to store the price data
        self.client = Client(pkey, skey)
        self.symbols = self.symbols #['BTCUSDT', 'ETHUSDT', 'XRPUSDT']  # You can define the symbols you need here
        self.bm = BinanceSocketManager(self.client)
        self.websocket_thread = None
        self.start_date = datetime(2021, 1, 1)
        self.end_date = datetime(2023, 7, 28)

    def load_historical_data(self):
        for symbol in self.symbols:
            # Umwandlung der Start- und Enddaten in Zeichenketten
            start_date_str = self.start_date.strftime('%Y-%m-%d %H:%M:%S')
            end_date_str = self.end_date.strftime('%Y-%m-%d %H:%M:%S')

            # Get historical price data from Binance API
            klines = self.client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, start_date_str, end_date_str)

            # Convert data to DataFrame
            df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'num_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            df.drop_duplicates(inplace=True)
            df.drop(columns=['close_time', 'quote_asset_volume', 'num_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'], inplace=True)

            # Add the 'symbol' column and store the symbol name in it
            df['symbol'] = symbol

            # Calculate Bollinger Bands
            df = initialize_bollinger_bands(df)

            # Save data to a SQLite database
            connection = sqlite3.connect('price_data.db')

            # Erstelle die Tabelle, falls sie noch nicht existiert
            df.to_sql('price_data', connection, if_exists='replace', index=True)

            # Füge die Daten in die vorhandene Tabelle ein
            df.to_sql('price_data', connection, if_exists='append', index=True)

            connection.close()

    def start_websocket(self):
        if self.websocket_thread is None:
            self.websocket_thread = threading.Thread(target=self._start_websocket)
            self.websocket_thread.start()

    def _start_websocket(self):
        # Start the Websocket for each symbol
        for symbol in self.symbols:
            self.bm.start_symbol_ticker_socket(symbol, self.process_message)
        self.bm.start()

    def process_message(self, msg):
        symbol = msg['s']
        price = float(msg['c'])
        volume = float(msg['v'])
        timestamp = msg['E'] / 1000
        dt = datetime.fromtimestamp(timestamp)
        
        # Add the new data to the dictionary
        self.data.setdefault(symbol, []).append((dt, price, volume))

        # Convert the data to DataFrame and calculate Bollinger Bands
        df = pd.DataFrame(self.data[symbol], columns=['timestamp', 'close', 'volume'])
        df.set_index('timestamp', inplace=True)
        df.drop_duplicates(inplace=True)
        df.dropna(inplace=True)
        df['close'] = pd.to_numeric(df['close'])

        # Calculate Bollinger Bands
        df = initialize_bollinger_bands(df)

        # Print Bollinger Band values for each symbol
        #print(f"--- Bollinger Bands for {symbol} ---")
        #print(df[['close', 'volume', 'bb_upperband', 'bb_middleband', 'bb_lowerband']])

        # Filter symbols based on bb_percentage_diff <= 4%
        buy_signal_df = df[df['bb_percentage_diff'] <= 0.04]

        # Calculate Kaufpreis
        buy_signal_df['kaufpreis'] = (buy_signal_df['close'] * 1.7) - buy_signal_df['close']

        # Print the filtered DataFrame
        print(f"--- Buy Signal for {symbol} ---")
        print(buy_signal_df)

        # Save data to a SQLite database
        connection = sqlite3.connect('price_data.db')
        df.to_sql('price_data', connection, if_exists='append', index=True)
        connection.close()

    def close_websocket(self):
        self.bm.stop()
        self.websocket_thread.join()

def initialize_bollinger_bands(df, window=20, window_dev=2):
    # Ensure the 'close' column is numeric and remove any rows with missing values
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    df.dropna(subset=['close'], inplace=True)

    indicator_bb = BollingerBands(close=df['close'], window=window, window_dev=window_dev)

    df['bb_upperband'] = indicator_bb.bollinger_hband()
    df['bb_middleband'] = indicator_bb.bollinger_mavg()
    df['bb_lowerband'] = indicator_bb.bollinger_lband()

    df['bb_lowerband_value'] = df['close'].iloc[-1]
    df['bb_upperband_value'] = df['close'].iloc[-1]

    # Calculate percentage difference between upper and lower bands
    df['bb_percentage_diff'] = (df['bb_upperband_value'] - df['bb_lowerband_value']) / 100

    return df

# Erstelle eine Instanz von PriceDataRetriever und lade historische Daten
data_retriever = PriceDataRetriever()
data_retriever.load_historical_data()
data_retriever.start_websocket()


