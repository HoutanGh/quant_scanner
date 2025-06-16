import pandas as pd
from data import fetch_yfinance_data
from tabulate import tabulate

def compute_trends(daily_df, minute_df, ref_time):
    exchange_tz = "America/New_York"  # Match the timezone used in data.py

    # Convert ref_time to pd.Timestamp and localize/convert to exchange timezone
    ref_time = pd.to_datetime(ref_time)
    if ref_time.tzinfo is None:
        ref_time = ref_time.tz_localize(exchange_tz)
    else:
        ref_time = ref_time.tz_convert(exchange_tz)

    # Filter daily and minute data up to ref_time
    daily_df = daily_df[daily_df['date'] <= ref_time]
    minute_df = minute_df[minute_df['date'] <= ref_time]

    periods = [
        ("1y", 252), ("6m", 126), ("60d", 60), ("1m", 21), ("1w", 5), ("1d", 1),
        ("12h", 12*60), ("6h", 6*60), ("3h", 3*60), ("1h", 60), ("30m", 30), ("15m", 15), ("1m", 1)
    ]
    results = []

    daily_close = daily_df.sort_values("date")["close"].reset_index(drop=True)
    for label, window in periods[:6]:
        if len(daily_close) >= window + 2:
            trend = (daily_close.iloc[-1] - daily_close.iloc[-window-1]) / window
            prev_trend = (daily_close.iloc[-window-1] - daily_close.iloc[-2*window-1]) / window
            double_deriv = (trend - prev_trend) / window
        else:
            trend = None
            double_deriv = None
        results.append((label, trend, double_deriv))

    minute_close = minute_df.sort_values("date")["close"].reset_index(drop=True)
    for label, window in periods[6:]:
        if len(minute_close) >= window + 2:
            trend = (minute_close.iloc[-1] - minute_close.iloc[-window-1]) / window
            prev_trend = (minute_close.iloc[-window-1] - minute_close.iloc[-2*window-1]) / window
            double_deriv = (trend - prev_trend) / window
        else:
            trend = None
            double_deriv = None
        results.append((label, trend, double_deriv))

    return results

def display_trends_table(stock, ref_time, results):
    print(f"\nStock: {stock}    Time: {ref_time}\n")
    df = pd.DataFrame(results, columns=["Period", "Trend", "Double Derivative"])
    print(tabulate(df, headers="keys", tablefmt="github", showindex=False))

if __name__ == "__main__":
    stock = "GME"
    ref_time = "2025-06-09 15:30:00"
    daily_df, minute_df = fetch_yfinance_data(stock, "2025-06-09")
    results = compute_trends(daily_df, minute_df, ref_time)
    display_trends_table(stock, ref_time, results)

