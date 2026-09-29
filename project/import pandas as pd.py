import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 获取AAPL在过去一年的历史数据
aapl = yf.Ticker("AAPL")
df = aapl.history(period="1y")

# 计算zigzag
import TradingView/ZigZag/6 as zigzag
zigZag = zigzag.newInstance(zigzag.Settings.new(0, 10, color(na), false, false, false, false, "Absolute", false))
if zigZag.update():
    pivots = zigZag.pivots
    pivotsCount = array.size(pivots)
    if pivotsCount > 1:
        p = pivots.get(pivotsCount - 2)
        lastP = p.end
        prevP = p.start
    if pivotsCount > 2:
        p2 = pivots.get(pivotsCount - 3)
        prev2P = p2.start
    ready = not(na(lastP) or na(prevP) or na(prev2P))

# 计算20日均线和50日均线
df['MA20'] = df['Close'].rolling(window=20).mean()
df['MA50'] = df['Close'].rolling(window=50).mean()

# 生成交易信号
df['Signal'] = 0
df['Signal'][df['MA20'] > df['MA50']] = 1
df['Signal'][df['MA20'] < df['MA50']] = -1

# 计算收益率
df['Returns'] = df['Close'].pct_change()
df['StrategyReturns'] = df['Returns'] * df['Signal'].shift(1)

# 设置每次交易5000股
df['Position'] = 5000 * df['Signal']

# 计算持仓和现金流
df['Position'] = df['Position'].fillna(method='ffill')
df['Cash'] = -1 * df['Position'] * df['Close']
df['Holdings'] = df['Position'] * df['Close']
df['Total'] = df['Cash'] + df['Holdings']

# 布林线策略
df['MA20'] = df['Close'].rolling(window=20).mean()
df['stddev'] = df['Close'].rolling(window=20).std()
df['Upper'] = df['MA20'] + (df['stddev'] * 2)
df['Lower'] = df['MA20'] - (df['stddev'] * 2)

# 交易策略
df['Buy'] = 0
df['Sell'] = 0
df['ClosePrice'] = df['Close']
df['Profit'] = 0
df['Buy'][df['Signal'] == 1] = df['Close']
df['Sell'][df['Signal'] == -1] = df['Close']
df['Buy'] = df['Buy'].fillna(method='ffill')
df['Sell'] = df['Sell'].fillna(method='ffill')
df['Profit'][df['Signal'] == 1] = df['Close'] - df['Buy']
df['Profit'][df['Signal'] == -1] = df['Sell'] - df['Close']
df['Profit'] = df['Profit'].fillna(0)
df['CumulativeProfit'] = df['Profit'].cumsum()

# zigzag交易策略
df['ZigZagSignal'] = 0
df['ZigZagSignal'][df['Close'] > lastP.price] = 1
df['ZigZagSignal'][df['Close'] < lastP.price] = -1
df['ZigZagSignal'] = df['ZigZagSignal'].fillna(method='ffill')
df['ZigZagPosition'] = 5000 * df['ZigZagSignal']
df['ZigZagPosition'] = df['ZigZagPosition'].fillna(method='ffill')
df['ZigZagCash'] = -1 * df['ZigZagPosition'] * df['Close']
df['ZigZagHoldings'] = df['ZigZagPosition'] * df['Close']
df['ZigZagTotal'] = df['ZigZagCash'] + df['ZigZagHoldings']
df['ZigZagReturns'] = df['Close'].pct_change()
df['ZigZagStrategyReturns'] = df['ZigZagReturns'] * df['ZigZagSignal'].shift(1)
df['ZigZagProfit'] = 0
df['ZigZagBuy'] = 0
df['ZigZagSell'] = 0
df['ZigZagBuy'][df['ZigZagSignal'] == 1] = df['Close']
df['ZigZagSell'][df['ZigZagSignal'] == -1] = df['Close']
df['ZigZagBuy'] = df['ZigZagBuy'].fillna(method='ffill')
df['ZigZagSell'] = df['ZigZagSell'].fillna(method='ffill')
df['ZigZagProfit'][df['ZigZagSignal'] == 1] = df['Close'] - df['ZigZagBuy']
df['ZigZagProfit'][df['ZigZagSignal'] == -1] = df['ZigZagSell'] - df['Close']
df['ZigZagProfit'] = df['ZigZagProfit'].fillna(0)
df['ZigZagCumulativeProfit'] = df['ZigZagProfit'].cumsum()

# 布林线策略下的交易
for i in range(len(df)):
    if df['Total'][i] > df['Upper'][i]:
        df['Position'][i] = -2500
    elif df['Total'][i] < df['Lower'][i]:
        df['Position'][i] = 2500

# zigzag策略下的交易
for i in range(len(df)):
    if df['ZigZagTotal'][i] > df['Upper'][i]:
        df['ZigZagPosition'][i] = -2500
    elif df['ZigZagTotal'][i] < df['Lower'][i]:
        df['ZigZagPosition'][i] = 2500

# 计算持仓和现金流
df['Position'] = df['Position'].fillna(method='ffill')
df['Cash'] = -1 * df['Position'] * df['Close']
df['Holdings'] = df['Position'] * df['Close']
df['Total'] = df['Cash'] + df['Holdings']