import yfinance as yf
import pandas_ta as ta

# Fetch stock data using yfinance


ticker = "ITC.NS"
df = yf.download(ticker, period="1mo", interval="15m")

# Calculate Supertrend (7, 3)
supertrend = ta.supertrend(df['High'], df['Low'], df['Close'], length=7, multiplier=3)
supertrend1 = ta.supertrend(df['High'], df['Low'], df['Close'], length=10, multiplier=3)

supertrend2 = ta.supertrend(df['High'], df['Low'], df['Close'], length=11, multiplier=2)


# Check the column names returned by supertrend function
print(supertrend.columns,supertrend1.columns,supertrend2.columns)

# Add the Supertrend values to the DataFrame
df['Supertrend'] = supertrend[supertrend.columns[0]]  # Use the correct column name dynamically
df['Supertrend1'] = supertrend1[supertrend1.columns[0]]
df['Supertrend2'] = supertrend2[supertrend2.columns[0]]

# Print the Supertrend values
print(df[['Close', 'Supertrend' , 'Supertrend1','Supertrend2']].tail())

# Print the latest Supertrend value
latest_value_0 = df['Supertrend'].iloc[-1]
latest_value_1 =df['Supertrend1'].iloc[-1]
latest_value_2 = df ['Supertrend'].iloc[-1]
print(f"Latest Supertrend (7,3): {latest_value_0}" , f"(10,3) : {latest_value_1}" , f"(11,2): {latest_value_2}")
