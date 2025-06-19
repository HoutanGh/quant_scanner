import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from data import fetch_yfinance_data

# Example: fetch data for AAPL
stock = "GME"
daily_df, minute_df = fetch_yfinance_data(stock, "2025-06-09")

# Convert date to timezone-naive for plotting
daily_df['plot_date'] = pd.to_datetime(daily_df['date']).dt.tz_localize(None)

# Plot daily price vs volume
fig, ax1 = plt.subplots(figsize=(12, 6))

# Format the x-axis to show dates nicely
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
plt.xticks(rotation=45)

# Plot the price line
color = 'tab:blue'
ax1.set_xlabel('Date')
ax1.set_ylabel('Close Price ($)', color=color)
ax1.plot(daily_df['plot_date'], daily_df['close'], color=color, label='Close Price')
ax1.tick_params(axis='y', labelcolor=color)

# Use a different approach for volume visualization
ax2 = ax1.twinx()
color = 'tab:orange'
ax2.set_ylabel('Volume', color=color)

# Convert volume to numpy array and ensure it's 1-dimensional
volume = daily_df['volume'].fillna(0).to_numpy()
dates = daily_df['plot_date'].to_numpy()

# Plot volume as a step chart with fill
ax2.step(dates, volume, color=color, alpha=0.7, where='mid', label='Volume')
ax2.tick_params(axis='y', labelcolor=color)

# Add a legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.title(f"{stock} Daily Close Price and Volume")
fig.tight_layout()
plt.show()