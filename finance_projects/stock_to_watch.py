

"""
yfinance.Ticker(ticker).history(start= , end= ) Get price + dividends + splits but only processes one ticker at a time.
['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
yfinance.download(tickers, start= , end= , ...) only daily prices and can process a list of ticksers
['Open', 'High', 'Low', 'Close', 'Volume']

"""



import datetime
import os
# Import packages
import yfinance as yf
import pandas as pd
import matplotlib as plt

# Define the ticker list
tickers_list = ['NBIS', 'QBTS', 'CRWV', 'OGN', 'WRD', 'PONY', 'ACHR', 'ONTO', 'NRG']
# days back from today
day_span = 31

# Set the start and end date
end_date = datetime.date.today() .strftime("%Y-%m-%d")
d1 = datetime.date.today() - timedelta(days=day_span)  # timespan of last 5 years
start_date = d1.strftime("%Y-%m-%d")



# Create placeholder for data
data = pd.DataFrame(columns=tickers_list)
# Fetch the data
for ticker in tickers_list:
    data[ticker] = yf.download(ticker, 
                               start_date,
                               end_date)['Close']
    
# Print first 5 rows of the data
data.head()

# Plot all the close prices
data.plot(figsize=(10, 7))
plt.legend()
plt.title("Close Price", fontsize=16)
plt.ylabel('Price', fontsize=14)
plt.xlabel('Year', fontsize=14)
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
plt.show()






from collections import OrderedDict
import numpy as np

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import yfinance as yf
from datetime import date, timedelta


from src.finance_playground.plot_utils import get_matplotlib_colors, plot_historical_price

end_date = date.today().strftime("%Y-%m-%d")
d1 = date.today() - timedelta(days=360 * 1)  # timespan of last 5 years
start_date = d1.strftime("%Y-%m-%d")


# collect all matplotlib colors
matplotlib_colors = OrderedDict()
# these colors can be called with a single character
matplotlib_colors.update(mcolors.BASE_COLORS)
# the default color cycle colors
matplotlib_colors.update(mcolors.TABLEAU_COLORS)
# named colors also recognized in css
matplotlib_colors.update(mcolors.CSS4_COLORS)
# named colors from the xkcd survey
matplotlib_colors.update(mcolors.XKCD_COLORS)

matplotlib_colors_list = list(matplotlib_colors.keys())
matplotlib_colors_list.remove("w")


company_symbol = {
    "Microsoft": "MSFT",
    "Alphabet": "GOOG",
    "Meta": "META",
    "Apple": "AAPL",
    "Amazon": "AMZN",
    "Array": "ARRY",
    "Enphase Energy": "ENPH",
    "American Airlines": "AAL",
    "Bayer": "BAYRY",
    "Kenvue": "KVUE",
}
# Let's call the API & get stock data
price_history = OrderedDict()

for company, symble in company_symbol.items():
    price_history[company] = yf.download(
        tickers=symble, start=start_date, end=end_date
    ).reset_index()

    # drop the unnecessary column index level   
    if len(price_history.columns.names) > 1:
        price_history.droplevel(level=1, axis=1)

    price_history[company].name = company



plot_historical_price(company_symbol,price_history)
plt.show()

import nasdaqdatalink
mydata = nasdaqdatalink.get("FRED/GDP")


import pandas_datareader.data as web
import pandas as pd
import datetime as dt

df = web.DataReader('GE', 'yahoo', start='2019-09-10', end='2019-10-09')

# drop the unnecessary column index level   
if len(df.columns.names) > 1:
    df=df.droplevel(level=1, axis=1)
df.head()
df = web.DataReader('005930', 'naver', start='2019-09-10', end='2019-10-09')



from polygon import RESTClient
client = RESTClient(api_key="iNopt7F73wQJt7Nh6_BkTydndWop42C5")

ticker = "AAPL"

# List Aggregates (Bars)
aggs = []
for a in client.list_aggs(ticker=ticker, multiplier=1, timespan="day", from_="2023-01-01", to="2023-06-13", limit=50000):
    aggs.append(a)

print(aggs)

# Get Last Trade
trade = client.get_last_trade(ticker=ticker)
print(trade)

# List Trades
trades = client.list_trades(ticker=ticker, timestamp="2022-01-04")
for trade in trades:
    print(trade)

# Get Last Quote
quote = client.get_last_quote(ticker=ticker)
print(quote)

# List Quotes
quotes = client.list_quotes(ticker=ticker, timestamp="2022-01-04")
for quote in quotes:
    print(quote)


