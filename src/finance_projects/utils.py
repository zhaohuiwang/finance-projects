"""
Utility functions classes to provide common and reusable functionalities for Finance projects.

By zhaohui Wang
Initiated on 06/13/2025
"""

from typing import List, Optional

from dataclasses import dataclass, field
from datetime import date, timedelta
import pandas as pd
import xarray
import yfinance


# Function to fetch data for a list of tickers and return as a Xarray.DataArray
def fetch_ticker_data(tickers: List[str], start_date: date, end_date: date) -> xarray.DataArray:
    """
    Fetch historical stock data from yfinance for a list of tickers
    Parameters:
    tickers: List[str]
        A list of tickers. For example, ['AAPL', 'MSFT', 'GOOGL', 'TSLA']
    start_date: date   
        For example, "2023-06-01"
    end_date: date
        For example, "2023-08-01"
    Return 
        xarray.DataArray

    Example:
    <xarray.Dataset> Size: 44kB
    Dimensions:       (time: 250, ticker: 3)
    Coordinates:
    * time          (time) datetime64[ns, America/New_York] 2kB 2023-01-03 00:0...
    * ticker        (ticker) object 24B 'AAPL' 'GOOGL' 'MSFT'
    Data variables:
        Open          (time, ticker) float64 6kB 128.6 89.06  ... 138.8 371.8
        High          (time, ticker) float64 6kB 129.2 90.51 ... 139.5 372.9
        Low           (time, ticker) float64 6kB 122.6 87.99  ... 138.0 369.3
        Close         (time, ticker) float64 6kB 123.5 88.59  ... 138.9 371.8
        Volume        (time, ticker) int64 6kB 112117500  ... 18723000
        Dividends     (time, ticker) float64 6kB 0.0 0.0  ... 0.0 0.0 0.0 0.0
        Stock Splits  (time, ticker) float64 6kB 0.0 0.0  ... 0.0 0.0 0.0 0.0

    Data variables: DataFrame Column index, distinct axis along which data varies
    Coordinates: pd.MultiIndex, label values along each dimension

    To subset
    xr_data["Close"].sel(ticker="AAPL", time=slice("2023-06-01", "2023-08-01"))
    xr_data.sel(ticker='AAPL', time=slice("2023-06-01", "2023-08-01"))['Close'].data

    yfinance.Ticker(ticker).history(start= , end= ) 
    -- Get price + dividends + splits but only processes one ticker at a time.
    ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']

    yfinance.download(tickers, start= , end= , ...) 
    -- only daily prices and can process a list of ticksers
    ['Open', 'High', 'Low', 'Close', 'Volume']

    """
    # Store results in a dictionary
    data_dict = {}

    for ticker in tickers:
        tkr = yfinance.Ticker(ticker)

        df = tkr.history(start=start_date, end=end_date, actions=True)
        if df.empty:
            raise ValueError(f"No data returned for ticker {ticker}")

        df["Ticker"] = ticker  # Add ticker column
        data_dict[ticker] = df

    # Combine into a single DataFrame
    combined_df = pd.concat(data_dict.values())
    combined_df = combined_df.reset_index().set_index(["Date", "Ticker"])

    # Unstack to get 3D shape: (Date, Ticker, Feature)
    df_unstacked = combined_df
    xr_data = df_unstacked.to_xarray()

    # Rename dims
    xr_data = xr_data.rename({"Date": "time", "Ticker":"ticker"})

    return xr_data

@dataclass
class StockData:
    """
    Stock data container with meta data attributes and data in Xarray.

    Usage example,
    stock_h = StockData(days_span=31)
    print(stock_h.data)
    """
    tickers_list: List[str] = field(default_factory=lambda: [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA' 
    ])
    variables_list: List[str] = field(default_factory=lambda: [
        'Close', 'Volume'
    ])
    end_date: date = field(default_factory=date.today)
    days_span: Optional[int] = None
    start_date: Optional[date] = None
    data: Optional[xarray.DataArray] = field(default=None, init=False)

    def __post_init__(self):
        # Validate inputs
        if self.days_span is None and self.start_date is None:
            raise ValueError("At least one of 'days_span' or 'start_date' must be specified")
        elif self.days_span is not None and self.start_date is None:
            self.start_date = self.end_date - timedelta(days=self.days_span)

        # Validate dates
        if self.start_date > self.end_date:
            raise ValueError("start_date must be before or equal to end_date")

        # Fetch data
        self.data = fetch_ticker_data(self.tickers_list, self.start_date, self.end_date)
        
        # Assign to data attribute
        self.data.attrs["source"] = "yfinance"
        self.data.attrs["tickers"] = self.tickers_list  
        self.data.attrs["start_date"] = self.start_date
        self.data.attrs["end_date"] = self.end_date

    def complete_date(self) -> 'StockData':
        """
        Return a new StockData with the same data (no string formatting needed).
        This method does nothing more besides wrappiong up all data variables may not be removed later once all possible sceneria test are completed.
        """
        return StockData(
            tickers_list=self.tickers_list,
            variables_list=self.variables_list,
            end_date=self.end_date,
            days_span=self.days_span,
            start_date=self.start_date,
            data=self.data
        )

