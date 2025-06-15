import pandas as pd
from data import fetch_yfinance_data 
from datetime import datetime

def get_trends_at_time(daily_df, minute_df, dt):
    """
    Given a datetime (dt), return percent change for each timeframe ending at dt.
    """
    # Ensure dt is a pandas Timestamp
    dt = pd.to_datetime(dt)

    # Find the closest available row in daily_df and minute_df
    daily_df = daily_df.copy()
    minute_df = minute_df.copy()
    daily_df['date'] = pd.to_datetime(daily_df['date'])
    minute_df['date'] = pd.to_datetime(minute_df['date'])

    # Helper to get close price at or before dt
    def get_close(df, delta):
        target = dt - delta
        df_before = df[df['date'] <= dt]
        df_target = df[df['date'] <= target]
        if df_before.empty or df_target.empty:
            return None, None
        close_now = df_before.iloc[-1]['close']
        close_then = df_target.iloc[-1]['close']
        return close_now, close_then

    trends = {}

    # Daily trends
    periods = [
        ('1y', pd.Timedelta(days=365)),
        ('6m', pd.Timedelta(days=182)),
        ('60d', pd.Timedelta(days=60)),
        ('1m', pd.Timedelta(days=21)),   # ~21 trading days in a month
        ('1w', pd.Timedelta(days=7)),
        ('1d', pd.Timedelta(days=1)),
    ]
    for label, delta in periods:
        now, then = get_close(daily_df, delta)
        if now is not None and then is not None and then != 0:
            trends[label] = 100 * (now - then) / then
        else:
            trends[label] = None

    # Minute trends
    periods_min = [
        ('1h', pd.Timedelta(hours=1)),
        ('15m', pd.Timedelta(minutes=15)),
        ('1m', pd.Timedelta(minutes=1)),
    ]
    for label, delta in periods_min:
        now, then = get_close(minute_df, delta)
        if now is not None and then is not None and then != 0:
            trends[label] = 100 * (now - then) / then
        else:
            trends[label] = None

    return trends


# Example usage in a new script or notebook



# Specify your stock and date/time
ticker = "GME"
end_date = "2025-06-09"  # The last date you want data for
target_datetime = "2025-06-09 15:30:00"  # The exact date and time for trend calculation

# Fetch data
daily_df, minute_df = fetch_yfinance_data(ticker, end_date)

# Get trends at the specified datetime
trends = get_trends_at_time(daily_df, minute_df, target_datetime)

# Print results
print(f"Trends for {ticker} at {target_datetime}:")
for tf, val in trends.items():
    if val is not None:
        print(f"{tf}: {val:.2f}%")
    else:
        print(f"{tf}: Not enough data")