import os
import requests
## value [4,3,2, -2, -3, -4]
def send_telegram_notification(symbol, value):
    # read Telegram Bot Token and Chat ID from environment variables
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    yahoo_fn_base_url = 'https://finance.yahoo.com/quote/'
    
    # Set the suggestion based on the value
    if value > 3:
        message = f"🟢Strong recommendation to buy \"{symbol}\"."
    elif value > 1:
        message = f"📈Recommendation to buy \"{symbol}\"."
    elif value < -3:
        message = f"🔴Strong recommendation to sell \"{symbol}\"."
    elif value < -1:
        message = f"📉Recommendation to sell \"{symbol}\"."
    else:
        message = "No valid recommendation."

    full_url = yahoo_fn_base_url + symbol
    full_url = full_url.encode('ascii', 'ignore').decode('ascii')
    # append yahoo_fn_base_url+ symbol to the message
    message = message + "\n\n\nMore detail here:\n" +full_url


    print(message)
    

    # Write the message to a text file
    with open('notification_message.txt', 'a') as file:
        file.write(message + '\n')

    
    if not bot_token or not chat_id:
        raise ValueError("🔴Error: Telegram Bot Token or Chat ID not set.")

    # Send a request to Telegram
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message
    }
    
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        print("Notification sent successfully.")
    else:
        print("🔴Error occurred while sending notification.")
        raise ValueError("🔴Error: Can not send msg to Telegram.")
