



"""
Pyhton code to process the Nationwide IUL transaction data resulting a pandas.DataFrame with structure like the following, 
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

try:
    df = pd.read_csv("/mnt/e/zhaohuiwang/dev/finance-projects/my_iuls/NW_IUL_transactions.csv")
except FileNotFoundError:
    print("File not found. Please check the file path.")

df["effective"] = pd.to_datetime(df["effective"], format="%m/%d/%Y")
df["processed"] = pd.to_datetime(df["processed"], format="%m/%d/%Y")


df["amount($)"] = df["amount($)"].replace({'\\$': '', '\\(': '-', '\\)': '', ',': ''}, regex=True).astype(float)


df["is_interest"] = df["type"].str.contains("Interest Credit", case=True, na=False)
df["is_segment_fee"] = df["type"].str.contains("Segment Fee", case=True, na=False)

df["is_monthly_deduction"] = df["type"].str.contains("Monthly Deduction", case=True, na=False)

df["is_payment"] = df["type"].str.contains("Payment", case=True, na=False)


# total payment

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