# Bollinger Bands Analysis Tool

## Description

The Bollinger Bands Analysis Tool is a Python-based project that helps analyze financial market data using Bollinger Bands. Bollinger Bands are a popular technical analysis tool used to identify potential price trends, volatility, and overbought or oversold conditions in financial markets. This tool retrieves price data from the Binance API, calculates Bollinger Bands, and provides insights on the percentage difference between the upper and lower bands for a given set of symbols.

## Features

- Retrieves price data from the Binance API
- Calculates Bollinger Bands (upper, middle, and lower bands)
- Calculates the percentage difference between the upper and lower bands
- Identifies potential buy signals based on a configurable threshold
- Sends buy signal notifications via Telegram

## How to Use

1. Clone the repository: `git clone <repository-url>`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Update the API keys in the `binanceapi.py` file with your Binance API credentials.
4. Specify the symbols you want to analyze in the `symbols.py` file.
5. Run the `auto_run.py` file to start the scheduled updates and analysis.
6. Update the `(bot_token, bot_chatID)` in the `tele.py` file with your Telegram credentials.

## Contact Information

For any inquiries or support, please contact:
- Rmana Issa
- [Project Repository](https://github.com/your-username/project-repo)

## License

This project is licensed under the [MIT License](LICENSE).
