import torchvision as tv
import pandas as pd
import matplotlib.pyplot as plt
import requests
import numpy as np
from tkinter import *

ALPHA_VANTAGE_API_KEY = '4EXGKTFBT7VMH4DR'

def bollinger_strategy(data, window):
    data['MA'] = data['Close'].rolling(window=window).mean()
    data['STD'] = data['Close'].rolling(window=window).std()
    data['Upper'] = data['MA'] + (data['STD'] * 2)
    data['Lower'] = data['MA'] - (data['STD'] * 2)
    data['BB_Signal'] = np.where(data['Close'] > data['Upper'], -1, np.where(data['Close'] < data['Lower'], 1, 0))
    return data

def moving_average_crossover(data, short_window, long_window):
    data['Short_MA'] = data['Close'].rolling(window=short_window).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window).mean()
    data['MA_Signal'] = np.where(data['Short_MA'] < data['Long_MA'], 1, np.where(data['Short_MA'] > data['Long_MA'], -1, 0))
    data['Crossover'] = data['MA_Signal'].diff()
    return data

def update_plot():
    stock_symbol = manual_entry.get()
    window = int(ma_entry.get())

    api_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(api_url)
    data = response.json()
    daily_data = data['Time Series (Daily)']
    dates = list(daily_data.keys())
    close_prices = [float(daily_data[date]['4. close']) for date in dates]

    df = pd.DataFrame({'Date': pd.to_datetime(dates), 'Close': close_prices})
    df.set_index('Date', inplace=True)

    bollinger_data = bollinger_strategy(df, window)
    crossover_data = moving_average_crossover(bollinger_data, window//2, window)

    fig, ax = plt.subplots()
    crossover_data[['Close', 'Short_MA', 'Long_MA', 'Upper', 'Lower']].plot(ax=ax)

    buy_bb = crossover_data[crossover_data['BB_Signal'] == 1]
    sell_bb = crossover_data[crossover_data['BB_Signal'] == -1]
    crossover_points = crossover_data[crossover_data['Crossover'] != 0]

    ax.scatter(buy_bb.index, buy_bb['Close'], color='green', marker='^', label='BB Buy Signal')
    ax.scatter(sell_bb.index, sell_bb['Close'], color='red', marker='v', label='BB Sell Signal')
    ax.scatter(crossover_points.index, crossover_points['Close'], color='blue', marker='o', label='MA Crossover Signal')

    ax.set_title(f'Bollinger Bands & MA Crossover for {stock_symbol}')
    ax.legend()
    plt.show()

root = Tk()
root.title("Stock Analysis")

Label(root, text="Stock Symbol:").pack()
manual_entry = Entry(root)
manual_entry.pack()

Label(root, text="MA Window Days:").pack()
ma_entry = Entry(root)
ma_entry.pack()

Button(root, text="Analyze", command=update_plot).pack()

root.mainloop()
