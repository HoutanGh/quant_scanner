import pandas as pd
import re
import os
import matplotlib.pyplot as plt

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
df = df.sort_values('Posted').reset_index(drop=True)

# Only create the CSV if it doesn't already exist
if not os.path.exists(csv_path):
    df.to_csv(csv_path, index=False)
    print(f"CSV created: {csv_path}")
else:
    print(f"CSV already exists: {csv_path}")

print(df.head())
print(len(df))  # total entries
print(len(df['Ticker'].unique()))  # unique tickers

# Extract day of week (Monday, Tuesday, etc.)
df['DayOfWeek'] = df['Posted'].dt.day_name()

# Count number of posts per day of week
counts = df['DayOfWeek'].value_counts()

# Reindex to get days in correct order
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
counts = counts.reindex(days_order)

# Plot bar chart
plt.figure(figsize=(10, 5))
counts.plot(kind='bar')
plt.xlabel('Day of Week')
plt.ylabel('Number of Tickers Posted')
plt.title('Number of Tickers Posted By Day of Week')
plt.tight_layout()
plt.show()