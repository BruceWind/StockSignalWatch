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

## Run it with Github-actions in schedule
1. Fork the Repository
First, fork this repository to your own GitHub account. This allows you to make changes and track your own version of the project.

2. Create a **Telegram Bot**
Next, you need to create a Telegram bot:

Open Telegram and search for the **BotFather**.
Start a chat with **BotFather** and use the command `/newbot` to create a new bot.
Follow the instructions to get your Bot Token.

3. Get Your **Chat ID**
To find your Chat ID:

Start a chat with your bot.
Send a message to the bot, then visit the following URL in your browser, replacing `YOUR_BOT_TOKEN` with your bot token:
Copy
https://api.telegram.org/bot{YOUR_BOT_TOKEN}/getUpdates
Look for the chat object in the JSON response to find your Chat ID.

4. Add **Variables** to GitHub
Return to your GitHub repository and add the following variables in the repository **settings**:

Navigate to **Settings** > **Actions** > **Variables**.
Add the following variables:
SYMBOL (your desired symbol)
TELEGRAM_CHAT_ID (your chat ID)
TELEGRAM_BOT_TOKEN (your bot token)

Like:
<img width="1131" alt="Screenshot 2024-07-22 at 11 39 02 AM" src="https://github.com/user-attachments/assets/4f12745a-ed88-4cf3-8f15-44eb8c8a264e">

After all, github actions will run this script in schedule. 

When the script believe you should **buy or sell**, it would send notification to telegram. Like:
<img width="757" alt="Screenshot 2024-07-22 at 12 03 58 PM" src="https://github.com/user-attachments/assets/81698389-99b9-4f58-ab8a-e8244afe0f04">

## License

[MIT](https://choosealicense.com/licenses/mit/)
