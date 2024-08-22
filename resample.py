import yfinance as yf
import pandas as pd

# Define the stock symbol and time period
symbol = 'LT.NS'  # Example: Apple Inc.
start_date = '2024-08-15'
end_date = '2024-08-21'

# Fetch historical data at 1-minute intervals
df = yf.download(symbol, start=start_date, end=end_date, interval='15m')

# Resample from 1-minute to 15-minute intervals
# df_resampled = df.resample('15min').agg({
#     'Open': 'first',
#     'High': 'max',
#     'Low': 'min',
#     'Close': 'last',
#     'Volume': 'sum'
# })




# Print the head of the resampled data
print("Head of Resampled Stock Data for 15-Minute Intervals:")
print(df[['Volume']].head())
