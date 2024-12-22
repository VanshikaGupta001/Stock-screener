import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
 

def fetch_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Function to calculate daily returns
def calculate_daily_returns(data):
    data['Daily Return'] = data['Adj Close'].pct_change()
    return data

# Function to calculate moving averages
def calculate_moving_averages(data, short_window, long_window):
    data['Short MA'] = data['Adj Close'].rolling(window=short_window).mean()
    data['Long MA'] = data['Adj Close'].rolling(window=long_window).mean()
    return data

# Function to calculate volatility (standard deviation of daily returns)
def calculate_volatility(data, window=21):
    data['Volatility'] = data['Daily Return'].rolling(window=window).std() * np.sqrt(window)
    return data

# Function to plot price and moving averages
def plot_data(data, ticker):
    plt.figure(figsize=(10, 6))
    plt.plot(data['Adj Close'], label='Adjusted Close Price', color='blue')
    plt.plot(data['Short MA'], label='Short-term Moving Average', color='red')
    plt.plot(data['Long MA'], label='Long-term Moving Average', color='green')
    plt.title(f'{ticker} Stock Price and Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend(loc='best')
    plt.grid(True)
    st.pyplot(plt)

# Function to plot daily returns and volatility
def plot_returns_volatility(data):
    fig, ax = plt.subplots(2, 1, figsize=(10, 10))

    # Plot Daily Returns
    ax[0].plot(data['Daily Return'], label='Daily Returns', color='purple')
    ax[0].set_title('Daily Returns')
    ax[0].set_ylabel('Daily Return')
    ax[0].legend()

    # Plot Volatility
    ax[1].plot(data['Volatility'], label='Volatility', color='orange')
    ax[1].set_title('Volatility')
    ax[1].set_ylabel('Volatility')
    ax[1].legend()

    plt.tight_layout()
    st.pyplot(plt)

def update(a):
    return st.slider(a)
    
# Streamlit
def main():
    st.title('Stock Price Analysis Tool')
    
    # User input for company selection and date range
    ticker = st.text_input('Enter Stock Ticker (e.g., AAPL, MSFT):\nrefer https://stockanalysis.com/stocks/ to get various tickers', 'AAPL' )
    start_date = st.date_input('Start Date', pd.to_datetime('2023-01-01'))
    end_date = st.date_input('End Date', pd.to_datetime('2024-01-01'))

    # Initialize sliders
    if 'short_window' not in st.session_state:
        st.session_state.short_window = 50
    if 'long_window' not in st.session_state:
        st.session_state.long_window = 200
    if 'volatility_window' not in st.session_state:
        st.session_state.volatility_window = 21

    # Financial Analysis Options
    short_window = st.slider('Short-term Moving Average Window', 10, 100, st.session_state.short_window)
    long_window = st.slider('Long-term Moving Average Window', 100, 300, st.session_state.long_window)
    volatility_window = st.slider('Volatility Window (days)', 10, 50, st.session_state.volatility_window)

    # Update new slider values
    st.session_state.short_window = short_window
    st.session_state.long_window = long_window
    st.session_state.volatility_window = volatility_window

    # "Analyze" button
    if st.button('Analyze'):
        data = fetch_data(ticker, start_date, end_date)
        len= (end_date-start_date).days

        if data.empty:
            st.error("No data found for the selected ticker and date range. Please try again.")
            return
        
        # Displaydata
        st.write(f"Showing stock data for {ticker} from {start_date} to {end_date}:")
        st.write(data.iloc[1: len: int(len/20)])
    

        # Calculate Metrics
        data = calculate_daily_returns(data)
        data = calculate_moving_averages(data, short_window, long_window)
        data = calculate_volatility(data, window=volatility_window)


        # Plot Data
        plot_data(data, ticker)
        plot_returns_volatility(data)
    
 


if __name__ == '__main__':
 main()

