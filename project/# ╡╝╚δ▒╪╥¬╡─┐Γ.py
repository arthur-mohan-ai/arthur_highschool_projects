import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import requests
from tkinter import ttk
PREDEFINED_STOCKS = {
    
    "MSFT": "Microsoft Corporation",
    "AAPL": "APPLE",
}
def bollinger_strategy(data, ma_days):
    
    data['MA' + str(ma_days)] = data['Close'].rolling(window=ma_days, min_periods=1).mean() # 计算均线
    data['std'] = data['Close'].rolling(window=ma_days, min_periods=1).std()
    data['Upper'] = data['MA' + str(ma_days)] + (data['std'] * 2)
    data['Lower'] = data['MA' + str(ma_days)] - (data['std'] * 2)
    return data
ALPHA_VANTAGE_API_KEY = '4EXGKTFBT7VMH4DR'
def update_plot():
    if manual_entry_var.get() == 1:
        stock_symbol = manual_entry.get()
    else:
        stock_symbol = stock_var.get()
    ma_days = int(ma_entry.get())
    api_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(api_url)
    data = response.json()
    if 'Time Series (Daily)' in data:
        daily_data = data['Time Series (Daily)']
        dates = list(daily_data.keys())
        close_prices = [float(daily_data[date]['4. close']) for date in dates]
        data = pd.DataFrame({'Date': pd.to_datetime(dates), 'Close': close_prices})
        data.set_index('Date', inplace=True)  
        data = bollinger_strategy(data, ma_days)
        ax.clear() 
        ax.plot(data.index, data['Close'], label='Close Price', linewidth=2.5)
        ax.plot(data.index, data['MA' + str(ma_days)], label=f'MA{ma_days}')
        ax.plot(data.index, data['Upper'], label='Upper Bollinger Band') 
        ax.plot(data.index, data['Lower'], label='Lower Bollinger Band')  
        ax.fill_between(data.index, data['Lower'], data['Upper'], color='gray', alpha=0.2) 
        ax.set_title(f'Bollinger Bands for {stock_symbol}')
        ax.legend() 
        if data['MA' + str(ma_days)].iloc[-1] > data['Upper'].iloc[-1]:
            signal = "Sell"
            ax.scatter(data.index[-1], data['Close'].iloc[-1], color='red', marker='v', label='Sell Signal')
            buy_sell_label.config(text="Red V: Sell Signal")
            sell_message = f"Bollinger Bands Sell Signal for {stock_symbol}: 收盘价触碰上轨!"
            requests.get(f"https://sc.ftqq.com/SCT226353TPuWnwx7fx1aftGR3C04wmCcX.send?text={sell_message}")

        elif data['MA' + str(ma_days)].iloc[-1] < data['Lower'].iloc[-1]:
            signal = "Buy"
            ax.scatter(data.index[-1], data['Close'].iloc[-1], color='green', marker='^', label='Buy Signal')
            buy_sell_label.config(text="Green ^: Buy Signal")
        else:
            signal = "Hold"
            buy_sell_label.config(text="")
        signal_label.config(text=f"Signal: {signal}")
        canvas.draw()
    else:
        signal_label.config(text="Invalid Symbol")
        buy_sell_label.config(text="")
        ax.clear()
        canvas.draw()



root = Tk()
root.title("Long Term Bollinger Bands Trading Strategy System")
root.configure(bg='lightblue')


test_button = Button(root, text="Test Server酱", command=test_server_chan)
test_button.pack(side=BOTTOM, pady=10)  
manual_entry_var = IntVar()
manual_entry_checkbox = Checkbutton(root, text="手动输入股票代码", variable=manual_entry_var)
manual_entry_checkbox.pack()

manual_entry = Entry(root, highlightbackground='lightblue')
manual_entry.pack()

stock_var = StringVar() 
for stock_code, stock_name in PREDEFINED_STOCKS.items():
    Radiobutton(root, text=f"{stock_code} - {stock_name}", variable=stock_var, value=stock_code).pack()
Label(root, text="").pack()

label = Label(root, text="Enter MA Days (e.g., 20):")
label.pack()

ma_entry = Entry(root)
ma_entry.pack()
Label(root, text="").pack()
plot_button = Button(root, text="Plot Bollinger Bands", command=update_plot, bg='blue', fg='white', font=('Arial', 14, 'bold'))
plot_button.pack(pady=10, ipadx=20, ipady=10)
fig = Figure(figsize=(6, 4), dpi=100) 
ax = fig.add_subplot(1, 1, 1)   
canvas = FigureCanvasTkAgg(fig, master=root)   
canvas_widget = canvas.get_tk_widget()    
canvas_widget.pack()                     
signal_label = Label(root, text="", font=("Arial", 14, "bold"))
signal_label.pack()
buy_sell_label = Label(root, text="", font=("Arial", 12, "italic"))
buy_sell_label.pack()
root.mainloop()