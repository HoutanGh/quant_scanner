import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from data import fetch_yfinance_data

stock = "OKYO"
daily_df, minute_df = fetch_yfinance_data(stock, "2025-06-21")

minute_df['plot_date'] = pd.to_datetime(minute_df['date']).dt.tz_localize(None)

# Filter for June 19th and 20th
start_date = pd.to_datetime("2025-06-19").date()
end_date = pd.to_datetime("2025-06-20").date()
mask = (minute_df['plot_date'].dt.date >= start_date) & (minute_df['plot_date'].dt.date <= end_date)
day_df = minute_df[mask]
print(day_df['plot_date'].min(), day_df['plot_date'].max())

# Print stats for the selected date range
print(f"Date range: {start_date} to {end_date}")
print(f"Total data points: {len(day_df)}")
print(f"Zero volume entries: {(day_df['volume'] == 0).sum()}")
print(f"Total volume: {day_df['volume'].sum()}")

fig, ax1 = plt.subplots(figsize=(16, 7))

# Plot close price
ax1.plot(day_df['plot_date'], day_df['close'], color='tab:blue', label='Close Price')
ax1.set_xlabel('Time')
ax1.set_ylabel('Price', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Format x-axis for time of day
ax1.xaxis.set_major_locator(mdates.DayLocator())
ax1.xaxis.set_minor_locator(mdates.HourLocator(interval=3))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax1.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=45)

# Add date separators
for date in pd.date_range(start=start_date, end=end_date):
    date = pd.Timestamp(date)
    ax1.axvline(x=date, color='gray', linestyle='--', alpha=0.5)

# Plot volume on secondary y-axis
ax2 = ax1.twinx()
ax2.plot(
    day_df['plot_date'],
    day_df['volume'],
    color='tab:orange',
    label='Volume',
    linewidth=1.5,
    alpha=0.8
)
ax2.set_ylabel('Volume', color='tab:orange')
ax2.tick_params(axis='y', labelcolor='tab:orange')

# Add legends and title
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

plt.title(f"{stock} Minute-by-Minute Price and Volume (June 19-20, 2025)")
plt.tight_layout()
plt.show()