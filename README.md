Crypto & Market Data Collector

A Python-based data pipeline that collects, processes, and prepares cryptocurrency, stock, and commodity data for AI price prediction training.
Features

    Multi-Asset Data Collection: Fetches historical data for cryptocurrencies, stocks (like NVIDIA), and gold prices

    Time Zone Support: Collects data with proper timezone awareness for accurate temporal analysis

    Automated Data Processing: Cleans, labels, and prepares raw market data for machine learning

    Flexible Output: Saves data in CSV or Excel format to your specified directory

    AI-Ready Datasets: Outputs structured data ready for training prediction models

Installation
bash

git clone https://github.com/yourusername/crypto-data-collector.git
cd crypto-data-collector
pip install -r requirements.txt

Quick Start
python

# Initialize data collector for Bitcoin
d = Get_crypto_data('BTC/USDT')

# Save data from specific start date with daily timeframe
S = d.Save_data('2024-01-01T00:00:00Z', timeframe='1d')

Usage Examples
Basic Cryptocurrency Data
python

# Get Bitcoin data
btc_data = Get_crypto_data('BTC/USDT')
btc_data.Save_data('2024-01-01T00:00:00Z', timeframe='1d', save_path='/path/to/your/data')

# Get Ethereum data
eth_data = Get_crypto_data('ETH/USDT')
eth_data.Save_data('2023-06-01T00:00:00Z', timeframe='4h')

Multiple Asset Types
python

# Get stock data (NVIDIA)
nvda_data = Get_stock_data('NVDA')
nvda_data.Save_data('2024-01-01T00:00:00Z', timeframe='1d')

# Get gold price data
gold_data = Get_commodity_data('GOLD')
gold_data.Save_data('2024-01-01T00:00:00Z', timeframe='1d')

Data Processing Pipeline

    Data Collection: Fetches raw OHLCV (Open, High, Low, Close, Volume) data from multiple sources

    Time Zone Normalization: Aligns timestamps across different markets and timezones

    Data Cleaning: Handles missing values, outliers, and inconsistencies

    Feature Labeling: Adds technical indicators and target variables for ML training

    Export: Saves structured datasets in your preferred format

Supported Timeframes

    1m - 1 minute

    5m - 5 minutes

    1h - 1 hour

    4h - 4 hours

    1d - 1 day

    1w - 1 week

Output Format

The script generates structured datasets with the following columns:

    Timestamp (timezone-aware)

    Open, High, Low, Close prices

    Volume

    Technical indicators (RSI, MACD, etc.)

    Labeled target variables for prediction

Requirements

    Python 3.8+

    pandas

    numpy

    ccxt (for cryptocurrency data)

    yfinance (for stock data)

    openpyxl (for Excel support)
