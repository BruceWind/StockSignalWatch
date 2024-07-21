import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from our_math import calculate_mean, calculate_median, find_third_smallest, find_smallest, find_largest, find_third_largest

def lowest_monthly_rsi(symbol):
  """Calculate the lowest RSI for each month over the last 12 months."""
  # Fetch data for the entire 12-month period
  end_date = datetime.now() - timedelta(days=5)
  start_date = end_date - timedelta(days=365)
  df = fetch_data_by_range(symbol, start_date, end_date)
  
  # Calculate RSI for the entire period
  df['RSI'] = calculate_rsi(df['Close'])
  
  # Group by month and get the lowest RSI
  monthly_lowest_rsi = df.groupby(pd.Grouper(freq='ME'))['RSI'].min()
  
  return monthly_lowest_rsi

def highest_monthly_rsi(symbol):
  """Calculate the highest RSI for each month over the last 12 months."""
  # Fetch data for the entire 12-month period

  end_date = datetime.now() - timedelta(days=5)
  start_date = end_date - timedelta(days=365)
  df = fetch_data_by_range(symbol, start_date, end_date)
  
  # Calculate RSI for the entire period
  df['RSI'] = calculate_rsi(df['Close'])
  
  # Group by month and get the highest RSI
  monthly_highest_rsi = df.groupby(pd.Grouper(freq='ME'))['RSI'].max()
  
  return monthly_highest_rsi

def lowest_monthly_cci(symbol):
    """Calculate the lowest CCI for each month over the last 12 months."""


    end_date = datetime.now() - timedelta(days=5)
    start_date = end_date - timedelta(days=365)
    df = fetch_data_by_range(symbol, start_date, end_date)
    
    # Calculate CCI for the entire period
    df['CCI'] = calculate_cci(df)
    
    # Group by month and get the lowest CCI
    monthly_lowest_cci = df.groupby(pd.Grouper(freq='ME'))['CCI'].min()
    
    return monthly_lowest_cci

def highest_monthly_cci(symbol):
    """Calculate the lowest CCI for each month over the last 12 months."""
    # Fetch data for the entire 12-month period
   
    end_date = datetime.now() - timedelta(days=5)
    start_date = end_date - timedelta(days=365)
    df = fetch_data_by_range(symbol, start_date, end_date)
    
    # Calculate CCI for the entire period
    df['CCI'] = calculate_cci(df)
    
    # Group by month and get the lowest CCI
    monthly_highest_cci = df.groupby(pd.Grouper(freq='ME'))['CCI'].max()
    
    return monthly_highest_cci


def calculate_monthly_low_average(data, column='Close'):
    """Calculate the average of monthly lows within the given period."""
    # Resample to monthly frequency and get the minimum
    monthly_lows = data[column].resample('M').min()
    # Calculate the average of these monthly lows
    return monthly_lows.mean()

## period can be:  ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
def fetch_data(symbol, period="1y"):
    """Fetch stock data."""
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period)
    return df


## e.g. for start & end with 5 days:
##      end_date = datetime.now() - timedelta(days=5)
##      start_date = end_date - timedelta(days=365)

def fetch_data_by_range(symbol, start=None, end=None):
    """Fetch stock data with custom date range."""
    ticker = yf.Ticker(symbol)
    df = ticker.history(start=start, end=end)
    return df



# def calculate_rsi(data, window=14):
    """Calculate RSI."""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


## middle value of CCI should be 50.
def calculate_rsi(data, window=14):
    """Calculate RSI."""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    # avoid devide by zero
    rs = gain / loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

## middle value of CCI should be 0.
def calculate_cci(data, window=20):
    """Calculate CCI."""
    tp = (data['High'] + data['Low'] + data['Close']) / 3
    sma = tp.rolling(window=window).mean()
    mad = tp.rolling(window=window).apply(lambda x: np.abs(x - x.mean()).mean())
    cci = (tp - sma) / (0.015 * mad)
    return cci

def main():
    # symbol = "APPL"  # Example: Apple Inc.
    symbol = "^SPX"
    # symbol = "QQQ"
    df = fetch_data(symbol)
    
    df['RSI'] = calculate_rsi(df['Close'])
    df['CCI'] = calculate_cci(df)
    
    latest_rsi = df['RSI'].iloc[-1]
    latest_cci = df['CCI'].iloc[-1]
    
    print(f"------------ RSI --------")
    
    monthly_lower_rsi_arr = lowest_monthly_rsi(symbol)
    print(f"Monthly lowest RSI for {symbol}:")
    print(monthly_lower_rsi_arr.to_string(float_format='{:.2f}'.format))


    monthly_highest_rsi_arr = highest_monthly_rsi(symbol)
    print(f"Monthly highest RSI for {symbol}:")
    print(monthly_highest_rsi_arr.to_string(float_format='{:.2f}'.format))

    highest = find_largest(monthly_highest_rsi_arr)
    third_highest = find_third_largest(monthly_highest_rsi_arr)

    print(f"Highest monthly RSI: {highest:.2f}")
    print(f"Third highest monthly RSI: {third_highest:.2f}")


    lowest = find_smallest(monthly_lower_rsi_arr)
    third_lowest = find_third_smallest(monthly_lower_rsi_arr)

    print(f"Lowest monthly RSI: {lowest:.2f}")
    print(f"Third lowest monthly RSI: {third_lowest:.2f}")

    print(f"Current RSI for {symbol}: {latest_rsi:.2f}")



    print(f"------------ CCI --------")

    ## it is an array 
    monthly_lower_cci_arr = lowest_monthly_cci(symbol)

    ## to filter cci is miner than -100
    # monthly_lower_cci_arr = monthly_lower_cci_arr[monthly_lower_cci_arr < -100]

    # print(f"Monthly lowest CCI for {symbol}:")
    # print(monthly_lower_cci_arr.to_string(float_format='{:.2f}'.format))



    monthly_highest_cci_arr = highest_monthly_cci(symbol)
    print(f"Monthly highest CCI for {symbol}:")
    print(monthly_highest_cci_arr.to_string(float_format='{:.2f}'.format))

    # median = calculate_median(monthly_highest_cci_arr)
    # print(f"Median monthly highest CCI for {symbol}: {median:.2f}")
    
    third_smallest = find_third_smallest(monthly_lower_cci_arr)
    print(f"Third smallest monthly lowest CCI for {symbol}: {third_smallest:.2f}")
    smallest_cci = find_smallest(monthly_lower_cci_arr)
    print(f"Smallest monthly lowest CCI for {symbol}: {smallest_cci:.2f}")

    ## largest and 3rd largest
    largest = find_largest(monthly_highest_cci_arr)
    print(f"Largest monthly lowest CCI for {symbol}: {largest:.2f}")
    third_largest = find_third_largest(monthly_highest_cci_arr)
    print(f"Third largest monthly lowest CCI for {symbol}: {third_largest:.2f}")
    print(f"Current CCI for {symbol}: {latest_cci:.2f}")

if __name__ == "__main__":
    main()
