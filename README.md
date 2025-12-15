This program backtests a simple moving average strategy for the EUR USD pair. 
To investigate the performance of this strategy total returns, sharpe ratio and maximum drawdown are calculated. 

An equity curve is generated tracking the cumulative value of our portfolio over time.
From this we can learn if the strategy is making money overall and the volatility of growth/loss. 
A smooth upward curve might indicate good risk adjusted performance whereas a sharp drop suggests large drawdowns and danger.

Sharpe ratio enable us to determine the return we get per unit of risk.
sharpe = (average return / volatility) x sqrt(num trading days)
We can tell the efficiency of our strategy and whether returns are worth the risk taken. A negative sharpe ratio would denote a losing strategy whereas a sharpe ratio value of above 2 indicates an excellent strategy (with the danger of being overfit).

Maximum drawdown gives us an idea of the worst possible loss of our approach.It enables us to find the worst potential loss if we bough at a peak and sold at the worst possible point afterwards. We first must find the peak experienced during our strategy. We then compare each point after this peak and ask how far below the peak we currently are.
Hence:
MDD = min((equity/peak)-1)
Essentially it captures the worst possible experience an investor may have. 