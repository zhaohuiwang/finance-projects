



"""
Pyhton code to process the Nationwide IUL transaction data resulting a pandas.The expected structure of the resulting DataFrame: 
>>> df.dtypes
effective               datetime64[ns]
processed               datetime64[ns]
type                            object
amount($)                      float64
is_interest                       bool
is_segment_fee                    bool
is_monthly_deduction              bool
is_payment                        bool
dtype: object
>>> 

"""


import pandas as pd

# Read the transactions data from a csv file into pandas dataframe
try:
    df = pd.read_csv("/mnt/e/zhaohuiwang/dev/finance-projects/my_iuls/NW_IUL_transactions.csv")
except FileNotFoundError:
    print("File not found. Please check the file path.")

# Convert two variables from string to pandas.Datetime
df["effective"] = pd.to_datetime(df["effective"], format="%m/%d/%Y")
df["processed"] = pd.to_datetime(df["processed"], format="%m/%d/%Y")

# In the original records, there was '$' prefix for all values in the transaction amount records. All deductions and fees are in parenthesis (to different from payment, interest earened). This line removes the '$' prefix, takes out each of the value from the parenthesis and prefixs it with a '-' character. The resulting values are then converted from string type to float. 
df["amount($)"] = df["amount($)"].replace({'\\$': '', '\\(': '-', '\\)': '', ',': ''}, regex=True).astype(float)

# Create new boolean indicator variables 
df["is_interest"] = df["type"].str.contains("Interest Credit", case=True, na=False)
df["is_segment_fee"] = df["type"].str.contains("Segment Fee", case=True, na=False)

df["is_monthly_deduction"] = df["type"].str.contains("Monthly Deduction", case=True, na=False)

df["is_payment"] = df["type"].str.contains("Payment", case=True, na=False)


# Summarize each of the categories
df[df["is_interest"]].reset_index(drop=True)['amount($)'].sum()
# 3882
df[df["is_payment"]].reset_index(drop=True)['amount($)'].sum()
# 89311
df[df["is_segment_fee"]].reset_index(drop=True)['amount($)'].sum()
# -2105
df[df["is_monthly_deduction"]].reset_index(drop=True)['amount($)'].sum()
# -7175
# total deduction and fees
-2105 - 7175 = -9280
# interest and payment
3882 + 89311 = 93193
# balance money in - money out
93193 -9280 = 83913
89311 + 3882 -2105 - 7175
78643.44 - 83913 