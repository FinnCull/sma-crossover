import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_data(ticker,start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

def add_sma_indicators(data, fast_window, slow_window):
    data["SMA_fast"] = data["Close"].rolling(window=fast_window).mean()
    data["SMA_slow"] = data["Close"].rolling(window=slow_window).mean()
    return data

def generate_positions(data):
    data["position"] = 0
    data.loc[data["SMA_fast"] > data["SMA_slow"], "position"]=1
    return data

def backtest_strategy(data):
    """
    Compute returns and cumulative performance for the strategy.
    """
    data["returns"] = data["Close"].pct_change().fillna(0)
    data["strategy_returns"] = (data["position"].shift(1) * data["returns"]).fillna(0)

    data["cumul_returns_buy_hold"] = (1 + data["returns"]).cumprod()
    data["cum_returns_strategy"] = (1 + data["strategy_returns"]).cumprod()
    return data

def plot_results(data,ticker,fast_window,slow_window):
    plt.style.use("ggplot")
    data[["Close", "SMA_fast", "SMA_slow"]].plot(figsize=(12, 6))
    plt.title(f"{ticker} Close Price with {fast_window}/{slow_window}-day SMAs")
    plt.show()
    data[["cumul_returns_buy_hold", "cum_returns_strategy"]].plot(figsize=(12, 6))
    plt.title("Buy & Hold vs SMA Crossover Strategy")
    plt.show()

def calculate_sharpe_ratio(data,trading_days):
    """
    sharpe = (mean excess return / std dev of returns) × sqrt(# periods per year)
    """
    strategy_daily_ret = data["strategy_returns"].dropna()
    mean_daily = strategy_daily_ret.mean()
    std_daily = strategy_daily_ret.std()
    sharpe_ratio = (mean_daily / std_daily) * np.sqrt(trading_days)
    return sharpe_ratio

def calculate_total_return(data):
    final_value = data["cum_returns_strategy"].iloc[-1]
    total_return = final_value - 1
    return total_return

def calculate_max_drawdown(data):
    equity_curve = data["cum_returns_strategy"].dropna()
    running_max = equity_curve.cummax()
    drawdown = equity_curve / running_max - 1.0
    max_drawdown = drawdown.min()
    return max_drawdown

if __name__ == "__main__":
    ticker = "EURUSD=X"
    start_date = "2015-01-01"
    end_date = "2025-01-01"
    fast_window = 10
    slow_window = 30
    trading_days = 252

    data = get_data(ticker,start_date,end_date)
    data = add_sma_indicators(data,fast_window,slow_window)
    data = generate_positions(data)
    data = backtest_strategy(data)

    plot_results(data,ticker,fast_window,slow_window)

    total_return = calculate_total_return(data)
    sharpe_ratio = calculate_sharpe_ratio(data,trading_days)
    max_drawdown = calculate_max_drawdown(data)

    print(f"Total Return: {total_return}\n" \
        f"Sharpe Ratio: {sharpe_ratio}\n" \
        f"Maximum Drawdown: {max_drawdown}")