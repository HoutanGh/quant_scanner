import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def format_yfinance_to_ikbr(ticker, end, start=None):
    if start is None:
        end_dt = pd.to_datetime(end)
        start = (end_dt - timedelta(days=365)).strftime('%Y-%m-%d')
    df = yf.download(ticker, start=start, end=end)
    
    # lower case for IKBR
    df = df.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    })

    # can also drop Adj Close but might even add this when getting data from IKBR  
    if "Adj Close" in df.columns:
        df = df.drop(columns=["Adj Close"])

    # Reset index if you want a column, or keep DatetimeIndex if matching to IBKR post-processed
    df.index.name = "date"
    df = df.reset_index()  # IBKR's util.df(bars) is a column, not an index
    
    # dummy columns for IBKR's optional fields
    df["averageWAP"] = None
    df["barCount"] = None

    # Reorder to IBKR style
    df = df[["date", "open", "high", "low", "close", "volume", "averageWAP", "barCount"]]
    
    return df

df = format_yfinance_to_ikbr("AAPL", "2024-01-01")
print(df.head())