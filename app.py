from flask import Flask, render_template, request, jsonify
import yfinance as yf
import pandas as pd
import pandas_ta as ta

app = Flask(__name__)

def get_stock_data(symbol, start_date, end_date, interval):
    stock = yf.Ticker(symbol)
    hist = stock.history(interval=interval, start=start_date, end=end_date)

    if hist.empty:
        raise ValueError(f"No data found for symbol: {symbol} in the given date range.")

    # Drop rows with NaN values in essential columns
    hist.dropna(subset=['High', 'Low', 'Close'], inplace=True)

    # Calculate volume spikes
    hist['Volume Spike'] = hist['Volume'] > hist['Volume'].rolling(window=20).mean() * 1.5

    # Reset index to ensure date/datetime is a column
    hist.reset_index(inplace=True)

    # Format date columns
    if 'Datetime' in hist.columns:
        hist['Datetime'] = hist['Datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
        date_column = 'Datetime'
    else:
        hist['Date'] = hist['Date'].dt.strftime('%Y-%m-%d')
        date_column = 'Date'

    # Calculate Supertrend
    try:
        hist['Supertrend_7_3'] = ta.supertrend(hist['High'], hist['Low'], hist['Close'], length=7, multiplier=3)['SUPERT_7_3']
    except Exception as e:
        print(f"Error calculating Supertrend (7,3): {e}")
        hist['Supertrend_7_3'] = None

    try:
        hist['Supertrend_10_3'] = ta.supertrend(hist['High'], hist['Low'], hist['Close'], length=10, multiplier=3)['SUPERT_10_3']
    except Exception as e:
        print(f"Error calculating Supertrend (10,3): {e}")
        hist['Supertrend_10_3'] = None

    try:
        hist['Supertrend_11_2'] = ta.supertrend(hist['High'], hist['Low'], hist['Close'], length=11, multiplier=2)['SUPERT_11_2']
    except Exception as e:
        print(f"Error calculating Supertrend (11,2): {e}")
        hist['Supertrend_11_2'] = None

    return hist, date_column

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['POST'])
def get_data():
    try:
        symbol = request.form.get('symbol').upper()
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        interval = request.form.get('interval')

        data, date_column = get_stock_data(symbol, start_date, end_date, interval)

        # Convert data to lists for Chart.js
        chart_data = {
            'dates': data[date_column].tolist(),
            'open': data['Open'].tolist(),
            'high': data['High'].tolist(),
            'low': data['Low'].tolist(),
            'close': data['Close'].tolist(),
            'volume': data['Volume'].tolist(),
            'supertrend_7_3': data['Supertrend_7_3'].tolist(),
            'supertrend_10_3': data['Supertrend_10_3'].tolist(),
            'supertrend_11_2': data['Supertrend_11_2'].tolist(),
        }

        return jsonify({'chart_data': chart_data})
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
