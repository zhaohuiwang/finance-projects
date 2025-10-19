
import os

import dotenv
from easydict import EasyDict
import schwabdev 


### Authorization
# Option I: input credential directly into the CLient()
# Option II: The function `load_dotenv`` loads environment variables from a .env file into your application's environment, making them accessible via os.getenv() or os.environ.By default, it looks for .env in the current directory.
dotenv.load_dotenv(
    #dotenv_path=dotenv_path,
    override=True,
    verbose=True
    )
print(f"Environment variables are loaded from {dotenv.find_dotenv()}")

client = schwabdev.Client(
    app_key=os.getenv('APP_KEY'),
    app_secret=os.getenv('APP_SECRET'),
    callback_url=os.getenv('CALLBACK_URL'),
    # where to save tokens
    tokens_file="schwab_ext/src/configs/.tokens.json"
    )
# The Schwab API uses two tokens to use the api:
# Refresh token - valid for 7 days, used to "refresh" the access token.
# Access token - valid for 30 minutes, used in all api calls.
    
# # Option III: through dotenv.dotenv_values()
# config = dotenv.dotenv_values(dotenv_path=dotenv_path)
# cfg = EasyDict(config)
# client = schwabdev.Client(
#     app_key=cfg.APP_KEY,
#     app_secret=cfg.APP_SECRET,
#     callback_url=cfg.CALLBACK_URL,
#     tokens_file=cfg.TOKEN_FILE_PATH
#     )


### Basic API calls
# get account number and hashes for linked accounts
linked_accounts = client.account_linked().json()
print(linked_accounts)
# select the first account to use for orders
account_hash = linked_accounts[0].get('hashValue')
# get positions for selected account
print(client.account_details(account_hash, fields="positions").json())
# get a list of quotes
print(client.quotes(["AAPL", "AMD"]).json())
# get an option chain
print(client.option_expiration_chain("AAPL").json())

### Order example
# place an order for INTC at limit price $10.00
# https://tylerebowers.github.io/Schwabdev/?source=pages%2Forders.html
order = {"orderType": "LIMIT", 
         #"orderType": "MARKET"
         "session": "NORMAL", 
         "duration": "DAY", 
         #"duration": "GOOD_TILL_CANCEL",
         "orderStrategyType": "SINGLE", 
         "price": '10.00',
         "orderLegCollection": [
             {"instruction": "BUY", 
              "quantity": 1, 
              "instrument": 
                  {"symbol": "INTC", 
                   "assetType": "EQUITY"
                   }
              }
         ]}
resp = client.order_place(account_hash, order)
print(f"Response code: {resp}") 
"""
There are five classes defined by the standard:
1xx informational response - the request was received, continuing process
2xx successful - the request was successfully received, understood, and accepted
3xx redirection - further action needs to be taken in order to complete the request
4xx client error - the request contains bad syntax or cannot be fulfilled
5xx server error - the server failed to fulfil an apparently valid request
"""

# get the order ID - if order is immediately filled then the id might not be returned
order_id = resp.headers.get('location', '/').split('/')[-1] 
print(f"Order id: {order_id}")
# cancel the order
print(client.order_cancel(account_hash, order_id))

### Streaming example
# create streamer
streamer = client.stream
# create a list to store responses
responses = []
def add_to_list(message):
    responses.append(message)
#start stream and send request
streamer.start(add_to_list)
streamer.send(streamer.level_one_equities("AMD", "0,1,2,3,4,5,6,7,8"))
#check responses REMEMBER: the stream is running in the background so the responses list will change on subsequent reruns)
print(responses)
#stop stream
streamer.stop()