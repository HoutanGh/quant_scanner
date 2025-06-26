import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from data import fetch_yfinance_data

def analyse_stock(ticker, start_date=None, end_date=None, combined_plot=True):
    """
    Analyse stock data and create plots of price and volume changes.
    
    Parameters:
    ticker (str): The stock ticker symbol
    start_date (str): Start date in format 'YYYY-MM-DD'
    end_date (str): End date in format 'YYYY-MM-DD'
    combined_plot (bool): Whether to show price and volume in a combined plot
    
    Returns:
    tuple: Daily and minute dataframes
    """

    # maybe set default date

    # Fetch data
    daily_df, minute_df = fetch_yfinance_data(ticker, end_date)
    
    # Format date for plotting
    minute_df['plot_date'] = pd.to_datetime(minute_df['date']).dt.tz_localize(None)
    
    # Filter for date range
    start_date_obj = pd.to_datetime(start_date).date()    
    end_date_obj = pd.to_datetime(end_date).date()
    
    mask = (minute_df['plot_date'].dt.date >= start_date_obj) & (minute_df['plot_date'].dt.date <= end_date_obj)
    day_df = minute_df[mask]
    
    print(f"Data range: {day_df['plot_date'].min()} to {day_df['plot_date'].max()}")
    
    # Calculate volume change
    day_df['volume_change'] = day_df['volume'].diff().fillna(0)
    
    if combined_plot:
        # Create combined plot with two y-axes
        fig, ax1 = plt.subplots(figsize=(14, 6))
        
        # Plot Close Price on primary y-axis
        ax1.plot(day_df['plot_date'], day_df['close'], label='Close Price', color='blue')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Price', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        
        # Format x-axis for time of day
        ax1.xaxis.set_major_locator(mdates.HourLocator(interval=1))
        ax1.xaxis.set_minor_locator(mdates.MinuteLocator(interval=15))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.xticks(rotation=45)
        
        # Plot Volume Change on secondary y-axis
        ax2 = ax1.twinx()
        ax2.plot(day_df['plot_date'], day_df['volume_change'], color='green', 
                label='Volume Change', linewidth=1.0, alpha=0.7)
        ax2.set_ylabel('Volume Change', color='green')
        ax2.tick_params(axis='y', labelcolor='green')
        
        # Legends
        lines_1, labels_1 = ax1.get_legend_handles_labels()
        lines_2, labels_2 = ax2.get_legend_handles_labels()
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')
        
        plt.title(f"{ticker} Price and Volume Change ({start_date} to {end_date})")
        plt.tight_layout()
        plt.show()
    
    else:
        # Create separate plots for price and volume change
        # Price plot
        plt.figure(figsize=(14, 6))
        plt.plot(day_df['plot_date'], day_df['close'], label='Close Price')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.title(f"{ticker} Minute-by-Minute Price ({start_date} to {end_date})")
        
        # Format x-axis for time of day
        ax = plt.gca()
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
        ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=15))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend()
        plt.show()
        
        # Volume change plot
        plt.figure(figsize=(14, 6))
        plt.plot(
            day_df['plot_date'], 
            day_df['volume_change'], 
            color='green', 
            label='Volume Change',
            linewidth=1.0,
            alpha=0.7
        )
        plt.ylabel('Volume Change', color='green')
        plt.xlabel('Time')
        plt.title(f"{ticker} Volume Change ({start_date} to {end_date})")
        plt.legend()
        plt.tight_layout()
        plt.show()
    
    return daily_df, day_df

if __name__ == "__main__":
    # Example usage when script is run directly
    analyse_stock("")
