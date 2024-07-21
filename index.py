import yfinance as yf
import pandas as pd
import numpy as np


def calculate_cci(data, period=20):
    """Calculate the Commodity Channel Index (CCI)."""
    typical_price = (data['High'] + data['Low'] + data['Close']) / 3
    sma = typical_price.rolling(window=period).mean()
    mad = typical_price.rolling(window=period).apply(lambda x: np.abs(x - x.mean()).mean())
    cci = (typical_price - sma) / (0.015 * mad)
    return cci

def lowest_monthly_cci(symbol):
    """Calculate the lowest CCI for each month over the last 12 months."""
    # Fetch data for the entire 12-month period
    df = fetch_data(symbol)
    
    # Calculate CCI for the entire period
    df['CCI'] = calculate_cci(df)
    
    # Group by month and get the lowest CCI
    monthly_lowest_cci = df.groupby(pd.Grouper(freq='ME'))['CCI'].min()
    
    return monthly_lowest_cci



def calculate_monthly_low_average(data, column='Close'):
    """Calculate the average of monthly lows within the given period."""
    # Resample to monthly frequency and get the minimum
    monthly_lows = data[column].resample('M').min()
    # Calculate the average of these monthly lows
    return monthly_lows.mean()

def calculate_avg_low_rsi(data, column='Close'):
    """Calculate a custom RSI-like indicator based on monthly lows."""
    monthly_low_avg = calculate_monthly_low_average(data, column)
    current_price = data[column].iloc[-1]
    
    # Calculate a simple ratio
    ratio = (current_price - monthly_low_avg) / monthly_low_avg
    
    # Convert to a 0-100 scale, similar to RSI
    custom_rsi = 100 * ratio / (1 + ratio)
    
    return min(max(custom_rsi, 0), 100)  # Ensure the result is between 0 and 100

def calculate_avg_low_cci(data, column='Close'):
    """Calculate a custom CCI-like indicator based on monthly lows."""
    monthly_low_avg = calculate_monthly_low_average(data, column)
    current_price = data[column].iloc[-1]
    
    # Calculate the mean absolute deviation of monthly lows
    monthly_lows = data[column].resample('M').min()
    mad = np.mean(np.abs(monthly_lows - monthly_low_avg))
    
    # Calculate a CCI-like value
    cci = (current_price - monthly_low_avg) / (0.015 * mad)
    
    return cci



## period can be:  ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
def fetch_data(symbol, period="6mo"):
    """Fetch stock data."""
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period)
    return df

def calculate_rsi(data, window=14):
    """Calculate RSI."""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

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
    symbol = "QQQ"
    df = fetch_data(symbol)
    
    df['RSI'] = calculate_rsi(df['Close'])
    df['CCI'] = calculate_cci(df)
    
    latest_rsi = df['RSI'].iloc[-1]
    latest_cci = df['CCI'].iloc[-1]




    custom_rsi = calculate_avg_low_rsi(df) # caculate the bound of low RSI
    custom_cci = calculate_avg_low_cci(df)# caculate the bound of low CCI
    
    print(f"Lower bound RSI for {symbol}: {custom_rsi:.2f}")
    print(f"Lower bound CCI for {symbol}: {custom_cci:.2f}")
    
    print(f"Current RSI for {symbol}: {latest_rsi:.2f}")
    print(f"Current CCI for {symbol}: {latest_cci:.2f}")

    ## it is an array 
    monthly_lower_cci_arr = lowest_monthly_cci(symbol)

    print(f"Monthly lowest CCI for {symbol}:")
    print(monthly_lower_cci_arr.to_string(float_format='{:.2f}'.format))

if __name__ == "__main__":
    main()
