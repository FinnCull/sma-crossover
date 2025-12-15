import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("ggplot")

ticker = "EURUSD=X"
start_date = "2015-01-01"
end_date = "2025-01-01"

data = yf.download(ticker, start=start_date, end=end_date)

# print(data.head())
# print(data.columns)

fast_window = 20
slow_window = 500

data["SMA_fast"] = data["Close"].rolling(window=fast_window).mean()
data["SMA_slow"] = data["Close"].rolling(window=slow_window).mean()

data[["Close", "SMA_fast", "SMA_slow"]].plot(figsize=(12, 6))

plt.title(f"{ticker} Close Price with {fast_window}/{slow_window}-day SMAs")
plt.show()

data["position"] = 0
data.loc[data["SMA_fast"] > data["SMA_slow"], "position"]=1

data["returns"] = data["Close"].pct_change().fillna(0)
data["strategy_returns"] = data["position"].shift(1)*data["returns"].fillna(0)

data["cumul_returns_buy_hold"] = (1 + data["returns"]).cumprod()
data["cum_returns_strategy"] = (1+data["strategy_returns"]).cumprod()

data[["cumul_returns_buy_hold","cum_returns_strategy"]].plot(figsize=(12,6))
plt.title("Buy & Hold vs SMA Crossover Strategy")
plt.show()

final_value = data["cum_returns_strategy"].iloc[-1]
total_return = final_value - 1
print("Total Return (strategy):", total_return)

#Sharpe = (mean excess return / std dev of returns) × sqrt(# periods per year)
strategy_daily_ret = data["strategy_returns"].dropna()

mean_daily = strategy_daily_ret.mean()
std_daily = strategy_daily_ret.std()

trading_days = 252
sharpe_ratio = (mean_daily / std_daily) * np.sqrt(trading_days)
print("sharpe ratio:",sharpe_ratio)

equity_curve = data["cum_returns_strategy"].dropna()

running_max = equity_curve.cummax()
drawdown = equity_curve / running_max - 1.0
max_drawdown = drawdown.min()
print("Max drawdown (strategy):", max_drawdown)

