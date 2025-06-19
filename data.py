import pandas as pd
import yfinance as yf
from datetime import timedelta
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

def fetch_yfinance_data(ticker, end, start=None):
    exchange_tz = "America/New_York"  # Adjust if you want to support other exchanges

    if start is None:
        end_dt = pd.to_datetime(end)
        start = (end_dt - timedelta(days=365)).strftime('%Y-%m-%d')
    
    # Fetch daily data
    daily_df = yf.download(ticker, start=start, end=end, interval="1d", auto_adjust=True)
    daily_df = daily_df.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    })
    if "Adj Close" in daily_df.columns:
        daily_df = daily_df.drop(columns=["Adj Close"])
    daily_df.index.name = "date"
    daily_df = daily_df.reset_index()
    
    # Handle timezone for daily data
    daily_df['date'] = pd.to_datetime(daily_df['date'])
    if daily_df['date'].dt.tz is None:
        daily_df['date'] = daily_df['date'].dt.tz_localize(exchange_tz)
    else:
        daily_df['date'] = daily_df['date'].dt.tz_convert(exchange_tz)
        
    daily_df["averageWAP"] = None
    daily_df["barCount"] = None
    daily_df = daily_df[["date", "open", "high", "low", "close", "volume", "averageWAP", "barCount"]]

    # Fetch minute data (max 7 days)
    end_dt = pd.to_datetime(end)
    minute_start = (end_dt - timedelta(days=6)).strftime('%Y-%m-%d')
    minute_df = yf.download(
        ticker,
        start=minute_start,
        end=end,
        interval="1m",
        auto_adjust=True
    )
    minute_df = minute_df.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    })
    if "Adj Close" in minute_df.columns:
        minute_df = minute_df.drop(columns=["Adj Close"])
    minute_df.index.name = "date"
    minute_df = minute_df.reset_index()
    
    # Handle timezone for minute data
    minute_df['date'] = pd.to_datetime(minute_df['date'])
    if minute_df['date'].dt.tz is None:
        minute_df['date'] = minute_df['date'].dt.tz_localize(exchange_tz)
    else:
        minute_df['date'] = minute_df['date'].dt.tz_convert(exchange_tz)
        
    minute_df["averageWAP"] = None
    minute_df["barCount"] = None
    minute_df = minute_df[["date", "open", "high", "low", "close", "volume", "averageWAP", "barCount"]]

    return daily_df, minute_df

# # Example usage:
# daily_df, minute_df = fetch_yfinance_data("AAPL", "2025-06-09")
# print(daily_df.head())
# print(minute_df.head())

# # Plot daily close and 7-day MA
# plt.figure(figsize=(12, 5))
# plt.plot(daily_df['date'], daily_df['close'], label='Daily Close')
# plt.plot(daily_df['date'], daily_df['close'].rolling(7).mean(), label='7-Day MA')
# plt.title('Daily Close and 7-Day MA')
# plt.legend()
# plt.show()

# # Plot minute close and 60-min MA (on last 2 days for clarity)
# recent_minute = minute_df[minute_df['date'] > minute_df['date'].max() - pd.Timedelta(days=2)]
# plt.figure(figsize=(12, 5))
# plt.plot(recent_minute['date'], recent_minute['close'], label='Minute Close')
# plt.plot(recent_minute['date'], recent_minute['close'].rolling(60).mean(), label='60-Min MA')
# plt.title('Minute Close and 60-Min MA (Last 2 Days)')
# plt.legend()
# plt.show()