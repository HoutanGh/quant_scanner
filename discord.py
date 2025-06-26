import pandas as pd
import re
import os
import matplotlib.pyplot as plt
from datetime import datetime
import pytz

file_path = 'discord_tickers.txt'
csv_path = 'discord_tickers.csv'

entries = []
ticker_pattern = re.compile(r'^Ticker:\s*(\S+)')
timestamp_pattern = re.compile(r'—\s*(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2})')

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

i = 0
while i < len(lines):
    m = ticker_pattern.match(lines[i])
    if m:
        ticker_raw = m.group(1)
        ticker = re.sub(r'[^A-Za-z0-9]', '', ticker_raw)
        timestamp = None
        j = i + 1
        while j < len(lines):
            tm = timestamp_pattern.search(lines[j])
            if tm:
                timestamp = tm.group(1)
                break
            j += 1
        entries.append({'Ticker': ticker, 'Posted': timestamp})
    i += 1

df = pd.DataFrame(entries)
df['Posted'] = pd.to_datetime(df['Posted'], format='%d/%m/%Y %H:%M', errors='coerce')

# Add timezone columns with proper names from the start
eastern = pytz.timezone('US/Eastern')
df['GMT'] = df['Posted'].dt.tz_localize('UTC')
df['EST'] = df['GMT'].dt.tz_convert(eastern)

# Add readable date and day columns
df['Date'] = df['GMT'].dt.strftime('%Y-%m-%d')
df['Day_of_Week'] = df['GMT'].dt.strftime('%A')
df['GMT'] = df['GMT'].dt.strftime('%H:%M')
df['EST'] = df['EST'].dt.strftime('%H:%M')

# Keep only the columns we want
df = df[['Ticker', 'Date', 'Day_of_Week', 'GMT', 'EST']].copy()

# Save the CSV
df.to_csv(csv_path, index=False)

print("Readable DataFrame:")
print(df.head())
print(f"Total entries: {len(df)}")
print(f"Unique tickers: {len(df['Ticker'].unique())}")

# Extract day of week for analysis - need to recreate this since we removed Posted column
df_temp = pd.DataFrame(entries)
df_temp['Posted'] = pd.to_datetime(df_temp['Posted'], format='%d/%m/%Y %H:%M', errors='coerce')
df_temp['DayOfWeek'] = df_temp['Posted'].dt.day_name()

# Count number of posts per day of week
counts = df_temp['DayOfWeek'].value_counts()

# Reindex to get days in correct order
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
counts = counts.reindex(days_order)

# # Plot bar chart
# plt.figure(figsize=(10, 5))
# counts.plot(kind='bar')
# plt.xlabel('Day of Week')
# plt.ylabel('Number of Tickers Posted')
# plt.title('Number of Tickers Posted By Day of Week')
# plt.tight_layout()
# plt.show()

# Show top tickers by frequency
print(f"\nMost frequent tickers:")
ticker_counts = df['Ticker'].value_counts().head(20)
for ticker, count in ticker_counts.items():
    print(f"  {ticker}: {count} posts")

# Show posting patterns by day
print(f"\nPosting patterns by day:")
day_counts = df['Day_of_Week'].value_counts().reindex(days_order)
for day, count in day_counts.items():
    if pd.notna(count):
        print(f"  {day}: {int(count)} posts")