import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime, timedelta
from data import fetch_yfinance_data
import matplotlib.ticker as mticker

def analyse_stock(ticker, date, time, target_date=None, combined_plot=True):
    """
    Analyse stock data around a specific date and time.
    
    Parameters:
    ticker (str): The stock ticker symbol
    date (str): Date in format 'YYYY-MM-DD'
    time (str): Time in format 'HH:MM'
    target_date (str): Optional target date to override the date range calculation
    combined_plot (bool): Whether to show price and volume in a combined plot
    
    Returns:
    tuple: Daily and minute dataframes
    """
    
    # Parse the input date and calculate date range
    if target_date == None:    
        target_date = pd.to_datetime(date).date()
        start_date = target_date - timedelta(days=1)
        end_date = target_date + timedelta(days=1)
        # Use original date and time for target line
        target_datetime = pd.to_datetime(f"{date} {time}")
        display_date = date
    else:
        target_date_parsed = pd.to_datetime(target_date).date()
        input_date_parsed = pd.to_datetime(date).date()
        
        # Check if target_date is within reasonable range of input date
        date_diff = abs((target_date_parsed - input_date_parsed).days)
        
        if date_diff > 3:  # If target_date is more than 3 days from input date
            print(f"Target date {target_date} is too far from input date {date}. Analysis cancelled.")
            return None, None
        else:
            start_date = target_date_parsed - timedelta(days=1)
            end_date = target_date_parsed + timedelta(days=1)
            # Use target_date with original time for target line
            target_datetime = pd.to_datetime(f"{target_date} {time}")
            display_date = target_date
    
    # Fetch data (use end_date + 1 to ensure we get all data)
    daily_df, minute_df = fetch_yfinance_data(ticker, str(end_date + timedelta(days=1)))
    
    # Format date for plotting
    minute_df['plot_date'] = pd.to_datetime(minute_df['date']).dt.tz_localize(None)
    
    # Filter for the 3-day range
    mask = (minute_df['plot_date'].dt.date >= start_date) & (minute_df['plot_date'].dt.date <= end_date)
    day_df = minute_df[mask]
    
    if day_df.empty:
        print(f"No data available for {ticker} in the specified date range")
        return daily_df, day_df
    
    # Calculate cumulative volume for each day
    day_df = day_df.copy()
    day_df['cumulative_volume'] = day_df.groupby(day_df['plot_date'].dt.date)['volume'].cumsum()
    
    if combined_plot:
        # Create combined plot with two y-axes
        fig, ax1 = plt.subplots(figsize=(16, 8))
        
        # Set grid background style
        ax1.grid(True, linestyle='-', alpha=0.7, color='white', linewidth=1.2)
        ax1.set_facecolor('#E6ECF7')  # Light gray background
        fig.patch.set_facecolor('white')
        
        # Remove spines (outline)
        for spine in ax1.spines.values():
            spine.set_visible(False)
        
        # Plot Close Price on primary y-axis
        ax1.plot(day_df['plot_date'], day_df['close'], label='Close Price', color='blue', linewidth=1.5)
        ax1.set_xlabel('Date and Time')
        ax1.set_ylabel('Price', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        
        # Add bold vertical line at target time
        ax1.axvline(x=target_datetime, color='white', linestyle='--', linewidth=3, alpha=0.9, 
                   label=f'Target Time ({display_date} {time})')
        ax1.axvline(x=target_datetime, color='darkgray', linestyle='--', linewidth=2, alpha=0.7)

        # Format x-axis with evenly spaced grid
        ax1.xaxis.set_major_locator(mdates.HourLocator(interval=6))
        ax1.xaxis.set_minor_locator(mdates.HourLocator(interval=2))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d\n%H:%M'))
        
        # Format y-axis with evenly spaced grid
        ax1.yaxis.set_major_locator(mticker.MaxNLocator(nbins=8))
        ax1.yaxis.set_minor_locator(mticker.MaxNLocator(nbins=16))
        
        plt.xticks(rotation=45)
        
        # Plot Cumulative Volume on secondary y-axis
        ax2 = ax1.twinx()
        ax2.plot(day_df['plot_date'], day_df['cumulative_volume'], color='green', 
                label='Cumulative Volume', linewidth=1.0, alpha=0.7)
        ax2.set_ylabel('Cumulative Volume', color='green')
        ax2.tick_params(axis='y', labelcolor='green')
        
        # Format y-axis for volume with evenly spaced grid
        ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=8))
        ax2.yaxis.set_minor_locator(mticker.MaxNLocator(nbins=16))
        
        # Remove spines for secondary axis too
        for spine in ax2.spines.values():
            spine.set_visible(False)
        
        # Legends
        lines_1, labels_1 = ax1.get_legend_handles_labels()
        lines_2, labels_2 = ax2.get_legend_handles_labels()
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')
        
        plt.title(f"{ticker} Price and Volume around {display_date} {time}")
        plt.tight_layout()
        plt.show()
    
    else:
        # Create separate plots for price and volume
        # Price plot
        fig1, ax = plt.subplots(figsize=(16, 6))
        
        # Set grid background style
        ax.grid(True, linestyle='-', alpha=0.7, color='white', linewidth=1.2)
        ax.set_facecolor('#2596be')  # Light gray background
        fig1.patch.set_facecolor('white')
        
        # Remove spines (outline)
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        ax.plot(day_df['plot_date'], day_df['close'], label='Close Price', linewidth=1.5)
        ax.axvline(x=target_datetime, color='white', linestyle='--', linewidth=3, alpha=0.9, 
                   label=f'Target Time ({display_date} {time})')
        ax.axvline(x=target_datetime, color='darkgray', linestyle='--', linewidth=2, alpha=0.7)
        ax.set_xlabel('Date and Time')
        ax.set_ylabel('Price')
        ax.set_title(f"{ticker} Price around {display_date} {time}")
        
        # Format axes with evenly spaced grid
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
        ax.xaxis.set_minor_locator(mdates.HourLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d\n%H:%M'))
        ax.yaxis.set_major_locator(mticker.MaxNLocator(nbins=8))
        ax.yaxis.set_minor_locator(mticker.MaxNLocator(nbins=16))
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend()
        plt.show()
        
        # Volume plot
        fig2, ax = plt.subplots(figsize=(16, 6))
        
        # Set grid background style
        ax.grid(True, linestyle='-', alpha=0.7, color='white', linewidth=1.2)
        ax.set_facecolor('#2596be')  # Light gray background
        fig2.patch.set_facecolor('white')
        
        # Remove spines (outline)
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        ax.plot(
            day_df['plot_date'], 
            day_df['volume'], 
            color='green', 
            label='Volume',
            linewidth=1.0,
            alpha=0.7
        )
        ax.axvline(x=target_datetime, color='white', linestyle='--', linewidth=3, alpha=0.9, 
                   label=f'Target Time ({display_date} {time})')
        ax.axvline(x=target_datetime, color='darkgray', linestyle='--', linewidth=2, alpha=0.7)
        ax.set_ylabel('Volume', color='green')
        ax.set_xlabel('Date and Time')
        ax.set_title(f"{ticker} Volume around {display_date} {time}")
        
        # Format axes with evenly spaced grid
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
        ax.xaxis.set_minor_locator(mdates.HourLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d\n%H:%M'))
        ax.yaxis.set_major_locator(mticker.MaxNLocator(nbins=8))
        ax.yaxis.set_minor_locator(mticker.MaxNLocator(nbins=16))
        
        plt.legend()
        plt.tight_layout()
        plt.show()
    
    return daily_df, day_df

def get_ticker_info(ticker):
    """
    Get ticker information from the CSV file.
    
    Parameters:
    ticker (str): The stock ticker symbol
    
    Returns:
    tuple: (ticker, date, time) that can be used directly with analyse_stock function
    """
    try:
        df = pd.read_csv('discord_tickers.csv')
        ticker_data = df[df['Ticker'].str.upper() == ticker.upper()]
        
        if ticker_data.empty:
            print(f"No data found for ticker: {ticker}")
            return None, None, None
        
        # Get the first (most recent) entry
        first_entry = ticker_data.iloc[0]
        return first_entry['Ticker'], first_entry['Date'], first_entry['GMT']
    
    except FileNotFoundError:
        print("discord_tickers.csv file not found")
        return None, None, None

if __name__ == "__main__":
    # Example usage when script is run directly
    stock = "VUZI"
    print(get_ticker_info(stock))
    ticker, date, time = get_ticker_info(stock)
    if ticker:
        analyse_stock(ticker, date, time, target_date="2025-07-03", combined_plot=True)
