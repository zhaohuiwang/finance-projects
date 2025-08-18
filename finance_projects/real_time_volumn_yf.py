import yfinance as yf
import time
import logging
# from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Twilio configuration (for SMS)
# TWILIO_ACCOUNT_SID = "your_twilio_account_sid"
# TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
# TWILIO_PHONE_NUMBER = "your_twilio_phone_number"
# YOUR_PHONE_NUMBER = "your_phone_number"

# Email configuration (for Gmail)
EMAIL_ADDRESS = "ezhwang@gmail.com"
EMAIL_PASSWORD = "amlx ohah wjls ozsy"
RECIPIENT_EMAIL = "ezhwang@gmail.com"

# Pushover configuration
PUSHOVER_USER_KEY = "ub8h75wkbpdfb3iia3nhsgd8fx4ge9"
PUSHOVER_API_TOKEN = "af5ceamcsm5hou6ff8axgbcom6vq6w"

# def send_sms_alert(message):
#     """Send SMS alert using Twilio."""
#     try:
#         client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#         client.messages.create(
#             body=message,
#             from_=TWILIO_PHONE_NUMBER,
#             to=YOUR_PHONE_NUMBER
#         )
#         logging.info("SMS alert sent successfully.")
#     except Exception as e:
#         logging.error(f"Failed to send SMS: {e}")

def send_email_alert(message):
    """
    Send email alert using SMTP.
    You need to setup App passwords and used it instead of your google account ligin password. 
    https://myaccount.google.com/apppasswords
    """
    try:
        msg = MIMEText(message)
        msg['Subject'] = 'Stock Volume Alert'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
        logging.info("Email alert sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

def send_pushover_alert(message):
    """Send push notification using Pushover."""
    try:
        response = requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": PUSHOVER_API_TOKEN,
                "user": PUSHOVER_USER_KEY,
                "message": message
            }
        )
        if response.status_code == 200:
            logging.info("Pushover alert sent successfully.")
        else:
            logging.error(f"Failed to send Pushover alert: {response.text}")
    except Exception as e:
        logging.error(f"Failed to send Pushover alert: {e}")

def monitor_stock_volumes(symbols, interval=60, volume_threshold=1.5):
    """
    Monitor trading volume for a list of stock symbols and send alerts on significant increases.
    
    Args:
        symbols (list): List of stock ticker symbols (e.g., ['AAPL', 'MSFT'])
        interval (int): Time interval between checks in seconds
        volume_threshold (float): Multiplier to detect significant volume increase
    """
    try:
        # Initialize stock objects and previous volume dictionary
        stocks = {symbol: yf.Ticker(symbol) for symbol in symbols}
        prev_volumes = {symbol: None for symbol in symbols}
        
        while True:
            for symbol in symbols:
                try:
                    # Fetch 1-minute interval data for the latest trading day
                    data = stocks[symbol].history(period="1d", interval="1m")
                    
                    if data.empty:
                        logging.warning(f"No data available for {symbol}. Market may be closed or symbol invalid.")
                        continue
                    
                    # Get the latest volume
                    current_volume = data['Volume'].iloc[-2]
                    # data['Volume'].iloc[-1] is always 0
                    
                    if prev_volumes[symbol] is not None:
                        # Check for significant volume increase
                        if current_volume > prev_volumes[symbol] * volume_threshold:
                            alert_message = (f"Volume spike detected for {symbol}! "
                                           f"Previous: {prev_volumes[symbol]}, Current: {current_volume}")
                            logging.info(alert_message)
                            # send_sms_alert(alert_message) # via Twilio
                            send_email_alert(alert_message) # via SMTP
                            send_pushover_alert(alert_message) # via Pushover
                    
                    # Update previous volume
                    prev_volumes[symbol] = current_volume
                    
                except Exception as e:
                    logging.error(f"Error fetching data for {symbol}: {e}")
            
            # Wait for the next tick
            time.sleep(interval)
            
    except Exception as e:
        logging.error(f"Failed to initialize stock monitoring: {e}")

if __name__ == "__main__":
    # Example usage
    stock_symbols = ["AAPL", "MSFT", "GOOGL"]  # Replace with desired stock tickers
    check_interval = 60    # Check every 60 seconds
    volume_spike_threshold = 1.5  # 50% increase in volume considered a spike
    
    monitor_stock_volumes(stock_symbols, check_interval, volume_spike_threshold)