import os
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from our_math import calculate_mean, calculate_median, find_third_smallest, find_smallest, find_largest, find_third_largest
from notifier import send_telegram_notification

def lowest_monthly_rsi(symbol):
  """Calculate the lowest RSI for each month over the last 12 months."""
  # Fetch data for the entire 12-month period
  end_date = datetime.now() - timedelta(days=5)
  start_date = end_date - timedelta(days=365)
  df = fetch_data_by_range(symbol, start_date, end_date)
  
  # Calculate RSI for the entire period
  df['RSI'] = calculate_rsi(df['Close'])
  
  # Group by month and get the lowest RSI
  monthly_lowest_rsi = df.groupby(pd.Grouper(freq='MS'))['RSI'].min()
  
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
  monthly_highest_rsi = df.groupby(pd.Grouper(freq='MS'))['RSI'].max()
  
  return monthly_highest_rsi

def lowest_monthly_cci(symbol):
    """Calculate the lowest CCI for each month over the last 12 months."""


    end_date = datetime.now() - timedelta(days=5)
    start_date = end_date - timedelta(days=365)
    df = fetch_data_by_range(symbol, start_date, end_date)
    
    # Calculate CCI for the entire period
    df['CCI'] = calculate_cci(df)
    
    # Group by month and get the lowest CCI
    monthly_lowest_cci = df.groupby(pd.Grouper(freq='MS'))['CCI'].min()
    
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
    monthly_highest_cci = df.groupby(pd.Grouper(freq='MS'))['CCI'].max()
    
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
    # symbol = "^SPX"

    symbol = os.getenv('SYMBOL')
    if not symbol:
        raise ValueError("🔴SYMBOL environment variable is not set.")
    # symbol = "QQQ"
    df = fetch_data(symbol)
    
    df['RSI'] = calculate_rsi(df['Close'])
    df['CCI'] = calculate_cci(df)
    
    latest_rsi = df['RSI'].iloc[-1]
    latest_cci = df['CCI'].iloc[-1]
    
    print(f"------------ RSI --------")
    
    monthly_lower_rsi_arr = lowest_monthly_rsi(symbol)
    # print(f"Monthly lowest RSI for {symbol}:")
    # print(monthly_lower_rsi_arr.to_string(float_format='{:.2f}'.format))


    monthly_highest_rsi_arr = highest_monthly_rsi(symbol)
    # print(f"Monthly highest RSI for {symbol}:")
    # print(monthly_highest_rsi_arr.to_string(float_format='{:.2f}'.format))

    highest_rsi = find_largest(monthly_highest_rsi_arr)
    third_highest_rsi = find_third_largest(monthly_highest_rsi_arr)

    print(f"Highest monthly RSI: {highest_rsi:.2f}")
    print(f"Third highest monthly RSI: {third_highest_rsi:.2f}")


    lowest_rsi = find_smallest(monthly_lower_rsi_arr)
    third_lowest_rsi = find_third_smallest(monthly_lower_rsi_arr)

    print(f"Lowest monthly RSI: {lowest_rsi:.2f}")
    print(f"Third lowest monthly RSI: {third_lowest_rsi:.2f}")

    print(f"Current RSI for {symbol}: {latest_rsi:.2f}")



    print(f"------------ CCI --------")

    ## it is an array 
    monthly_lower_cci_arr = lowest_monthly_cci(symbol)

    ## to filter cci is miner than -100
    # monthly_lower_cci_arr = monthly_lower_cci_arr[monthly_lower_cci_arr < -100]

    # print(f"Monthly lowest CCI for {symbol}:")
    # print(monthly_lower_cci_arr.to_string(float_format='{:.2f}'.format))



    monthly_highest_cci_arr = highest_monthly_cci(symbol)
    # print(f"Monthly highest CCI for {symbol}:")
    # print(monthly_highest_cci_arr.to_string(float_format='{:.2f}'.format))

    # median = calculate_median(monthly_highest_cci_arr)
    # print(f"Median monthly highest CCI for {symbol}: {median:.2f}")
    
    third_smallest_cci = find_third_smallest(monthly_lower_cci_arr)
    print(f"Third smallest monthly lowest CCI for {symbol}: {third_smallest_cci:.2f}")
    smallest_cci = find_smallest(monthly_lower_cci_arr)
    print(f"Smallest monthly lowest CCI for {symbol}: {smallest_cci:.2f}")

    ## largest and 3rd largest
    largest_cci = find_largest(monthly_highest_cci_arr)
    print(f"Largest monthly lowest CCI for {symbol}: {largest_cci:.2f}")
    third_largest_cci = find_third_largest(monthly_highest_cci_arr)
    print(f"Third largest monthly lowest CCI for {symbol}: {third_largest_cci:.2f}")
    print(f"Current CCI for {symbol}: {latest_cci:.2f}")


    ## to calculate value for notification.
    value = 0
    if latest_cci > largest_cci: value += 2
    elif latest_cci > third_largest_cci: value += 1
    elif latest_cci < smallest_cci: value -=2
    elif latest_cci < third_smallest_cci: value -=1

    if latest_rsi > highest_rsi: value += 2
    elif latest_rsi > third_highest_rsi: value += 1
    elif latest_rsi < lowest_rsi: value -=2
    elif latest_rsi < third_lowest_rsi: value -=1

    print(f"Value: {value}")

    ## math .abs value 
    if abs(value) > 1:
        send_telegram_notification(symbol, value)

if __name__ == "__main__":
    main()
