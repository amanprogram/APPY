import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Set the title of the app
st.title('Simple Moving Average (SMA) Crossover Strategy')

# Get user input for stock symbol and date range
symbol = st.text_input('Stock Symbol', 'AAPL')
start_date = st.date_input('Start Date', pd.to_datetime('2020-01-01'))
end_date = st.date_input('End Date', pd.to_datetime('2023-01-01'))

# Fetch the data
data = yf.download(symbol, start=start_date, end=end_date)

# Define the short-term and long-term windows
short_window = 50
long_window = 200

# Calculate the moving averages
data['SMA_50'] = data['Close'].rolling(window=short_window,
                                       min_periods=1).mean()
data['SMA_200'] = data['Close'].rolling(window=long_window,
                                        min_periods=1).mean()

# Generate signals
data['Signal'] = 0
data['Signal'][short_window:] = np.where(
    data['SMA_50'][short_window:] > data['SMA_200'][short_window:], 1, 0)
data['Position'] = data['Signal'].diff()

# Calculate daily returns
data['Return'] = data['Close'].pct_change()

# Calculate strategy returns
data['Strategy_Return'] = data['Return'] * data['Position'].shift(1)

# Calculate cumulative returns
data['Cumulative_Return'] = (1 + data['Strategy_Return']).cumprod()
data['Cumulative_Market_Return'] = (1 + data['Return']).cumprod()

# Plot the closing prices and moving averages
fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(data['Close'], label='Close Price')
ax.plot(data['SMA_50'], label='50-Day SMA', alpha=0.7)
ax.plot(data['SMA_200'], label='200-Day SMA', alpha=0.7)

# Plot buy signals
ax.plot(data[data['Position'] == 1].index,
        data['SMA_50'][data['Position'] == 1],
        '^',
        markersize=10,
        color='g',
        lw=0,
        label='Buy Signal')

# Plot sell signals
ax.plot(data[data['Position'] == -1].index,
        data['SMA_50'][data['Position'] == -1],
        'v',
        markersize=10,
        color='r',
        lw=0,
        label='Sell Signal')

ax.set_title(f'{symbol} Price and SMA Crossover Signals')
ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.legend()

st.pyplot(fig)

# Plot cumulative returns
fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(data['Cumulative_Return'], label='Strategy Return')
ax.plot(data['Cumulative_Market_Return'], label='Market Return')

ax.set_title('Cumulative Returns')
ax.set_xlabel('Date')
ax.set_ylabel('Cumulative Return')
ax.legend()

st.pyplot(fig)
