# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 20:28:36 2020

@author: Family_Optiplex9
pip install pip install pyportfolioopt


changes needed
https://stackoverflow.com/questions/63894169/pandas-datareader-importerror-cannot-import-name-urlencode
https://github.com/pydata/pandas-datareader/pull/793/commits/558862104028dd7dbf5e845b3b6c5fcfc0d568e5


"""


# pip install yfinance
# pip install fix_yahoo_finance

from pandas_datareader import data as web

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight') 


# get the stock symbols in the portfolio
assets = ['FB', 'AMZN', 'AAPL', 'GOOG', 'TSLA']
# wight
weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2])

stock_start_date = '2013-01-01'

today = datetime.today().strftime("%Y-%m-%d")
today = '2020-03-22'


df = pd.DataFrame()

# store the adjusted close proce to the stock into the DataFrame
for stock in assets:
    df[stock] = web.DataReader(stock,
                               data_source='yahoo',
                               start=stock_start_date,
                               end=today)['Adj Close']

my_stocks = df

# visually show the stock/portfolio
title = 'portfolio Adj. Close Price History'

for c in my_stocks.columns.to_numpy():
    plt.plot(my_stocks[c], label=c)
    
plt.title(title)
plt.xlabel('Date', fontsize=18)
plt.ylabel('Adj. Price ', fontsize=18)
plt.legend(my_stocks.columns.to_numpy(), loc='upper left')
plt.show()

# show the daily simple return
returns = df.pct_change()
returns

# create and show the annualized covariance matrix
# square root of the variance is the volatility 
cov_matrix_annual = returns.cov() * 252  # working days in a year
cov_matrix_annual

# calculate the portfolio variance
# the weight transposed times covariance matrix times the weight
port_variance = np.dot(weights.T, np.dot(cov_matrix_annual, weights))
port_variance

# calculate the portfolio volatility aka standard deviation
port_volatility = np.sqrt(port_variance)
port_volatility

# calculate the annual portfolio return
portfolio_simple_return = np.sum(returns.mean()*weights) * 252
portfolio_simple_return 

# show the expected annual return, volatility(risk) and variance
percent_var = str(round(port_variance, 2) * 100) + '%'
percent_vols = str(round(port_volatility, 2) * 100) + '%'
percent_ret = str(round(portfolio_simple_return, 2) * 100) + '%'

print(f'Expected annual return: {percent_ret}')
print(f'Annual volatility/risk: {percent_vols}')
print(f'Annual variance: {percent_var}')


# https://pypi.org/project/pyportfolioopt/

from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns



# calculate the exptected returns and 
# the annualized covariance matrix asset returns
mu = expected_returns.mean_historical_return(df)
S = risk_models.sample_cov(df)

# optimize for max sharp ratio (by William Sharp)



df = pd.DataFrame({"B": [0, 1, 2, np.nan, 4]})
df.expanding(2).sum()

DataFrame.rolling(window, min_periods=None, center=False,
                  win_type=None, on=None, axis=0, closed=None)
provide rolling window calculations.

df.rolling(2).sum()




import requests

url = "https://grok.com"
response = requests.get(url)

# Content
print(response.text)  # HTML content as a string
print(response.content)  # HTML content as bytes

# Metadata
print(response.status_code)  # e.g., 200
print(response.headers)  # e.g., {'content-type': 'text/html; charset=utf-8', ...}
print(response.url)  # https://grok.com
print(response.encoding)  # utf-8

"""
Response Content:
Text (response.text): The HTML content of the Grok homepage. This includes the page's structure, text, and elements like the header, footer, and main content describing Grok (e.g., information about the AI, subscription plans, and links to xAI resources). The content is encoded in UTF-8.

Raw Bytes (response.content): The raw binary representation of the HTML, useful if you need to process it as bytes.

JSON (response.json()): Not applicable here, as the response is HTML, not JSON. Attempting this would raise a requests.exceptions.JSONDecodeError.

Metadata:
Status Code (response.status_code): Likely 200 (OK), assuming the request succeeds.

Headers (response.headers): Includes details like:
Content-Type: Likely text/html; charset=utf-8.
Server: Information about the server hosting the site.
Other headers like Date, Content-Length, or caching directives.

URL (response.url): Should remain https://grok.com unless redirected.

Encoding (response.encoding): Typically utf-8 for HTML pages.

Cookies (response.cookies): Any cookies set by the server (e.g., for session tracking or analytics).

Elapsed Time (response.elapsed): Time taken for the server to respond.

History (response.history): Empty unless the request was redirected (e.g., from http to https).
"""