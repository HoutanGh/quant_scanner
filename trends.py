import pandas as pd
from data import fetch_yfinance_data
from tabulate import tabulate
import warnings

warnings.filterwarnings("ignore", category=FutureWarning, module="tabulate")


periods = [
        ("1y", 252),         # 252 trading days ~ 1 year
        ("6m", 126),         # 126 trading days ~ 6 months
        ("60d", 60),         # 60 trading days
        ("1m", 21),          # 21 trading days ~ 1 month
        ("1w", 5),           # 5 trading days ~ 1 week
        ("1d", 1),           # 1 trading day
        ("12h", 12*60),      # 12 hours in minutes
        ("6h", 6*60),        # 6 hours in minutes
        ("3h", 3*60),        # 3 hours in minutes
        ("1h", 60),          # 1 hour in minutes
        ("30m", 30),         # 30 minutes
        ("15m", 15),         # 15 minutes
        ("1m", 1),           # 1 minute
    ]


def compute_price_trends(daily_df, minute_df, periods):
    # Define periods in minutes and days
    
    price_trends = []

    # For daily periods
    daily_close = daily_df.sort_values("date")["close"].reset_index(drop=True)
    for label, window in periods[:6]:
        if len(daily_close) >= window + 1:
            price_trend = float(daily_close.iloc[-1] - daily_close.iloc[-window-1]) / window
        else:
            price_trend = None
        if isinstance(price_trend, pd.Series) and len(price_trend) == 1:
            price_trend = price_trend.iloc[0]
        price_trends.append((label, price_trend))

    # For intraday periods (minute_df)
    minute_close = minute_df.sort_values("date")["close"].reset_index(drop=True)
    for label, window in periods[6:]:
        if len(minute_close) >= window + 1:
            price_trend = float(minute_close.iloc[-1] - minute_close.iloc[-window-1]) / window
        else:
            price_trend = None
        if isinstance(price_trend, pd.Series) and len(price_trend) == 1:
            price_trend = price_trend.iloc[0]
        price_trends.append((label, price_trend))

    return price_trends

def compute_volume_trends(daily_df, minute_df, periods):
    volume_trends = []

    # For daily periods
    daily_volume = daily_df.sort_values("date")["volume"].reset_index(drop=True)
    for label, window in periods[:6]:
        if len(daily_volume) >= window + 1:
            volume_trend = float(daily_volume.iloc[-1] - daily_volume.iloc[-window-1]) / window
        else:
            volume_trend = None
        if isinstance(volume_trend, pd.Series) and len(volume_trend) == 1:
            volume_trend = volume_trend.iloc[0]
        volume_trends.append((label, volume_trend))

    # For intraday periods (minute_df)
    minute_volume = minute_df.sort_values("date")["volume"].reset_index(drop=True)
    for label, window in periods[6:]:
        if len(minute_volume) >= window + 1:
            volume_trend = float(minute_volume.iloc[-1] - minute_volume.iloc[-window-1]) / window
        else:
            volume_trend = None
        if isinstance(volume_trend, pd.Series) and len(volume_trend) == 1:
            volume_trend = volume_trend.iloc[0]
        volume_trends.append((label, volume_trend))

    return volume_trends


def display_trends_table(stock, trends):
    df = pd.DataFrame(trends, columns=["Period", "Trend"])
    df.insert(0, "Stock", stock)
    print(tabulate(df, headers="keys", tablefmt="github", showindex=False))



if __name__ == "__main__":
    stock = "GME"
    daily_df, minute_df = fetch_yfinance_data(stock, "2025-06-09")
    price_trends = compute_price_trends(daily_df, minute_df, periods)
    volume_trends = compute_volume_trends(daily_df, minute_df, periods)
    display_trends_table(stock, price_trends)
    display_trends_table(stock, volume_trends)
