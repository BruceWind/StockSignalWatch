## StockSignalWatch


StockSignalWatch is a Python-based tool for analyzing stock market data and generating technical indicators. It focuses on calculating and monitoring RSI (Relative Strength Index) and CCI (Commodity Channel Index) for specified stocks.

## Features

- Fetch real-time stock data using yfinance
- Calculate RSI (Relative Strength Index)
- Calculate CCI (Commodity Channel Index)
- Customizable time period for data fetching
- Adjustable window sizes for RSI and CCI calculations

## Technologies Used

- Python 3
- yfinance: For fetching stock market data
- pandas: For data manipulation and analysis
- numpy: For numerical operations


## Run it locally

``` shell
 ## see doc: https://docs.python.org/3/library/venv.html#creating-virtual-environments
python3 -m venv myenv ## only init at first time.
source myenv/bin/activate
pip install --use-pep517 -r requirements.txt ## only install at first time.
python index.py

## exist python env
deactivate
```



## License

[MIT](https://choosealicense.com/licenses/mit/)
