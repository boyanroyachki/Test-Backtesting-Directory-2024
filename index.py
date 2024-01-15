from backtesting import Backtest, Strategy
from backtesting.test import GOOG

import talib
from backtesting.lib import crossover

#print(GOOG)
#all prices are in US Dollars

class RsiOscillator(Strategy): 

    #very standart values
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    #takes price and the window
    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_window)


    #goes through each candle and evaluates the criteria
    def next(self):
        #sell
        if crossover(self.rsi, self.upper_bound):
            self.position.close()

        #buy
        elif crossover(self.lower_bound, self.rsi):
            self.buy()

#can add comision, but will leave it for now
bt = Backtest(GOOG, RsiOscillator, cash = 10_000)

#stats = bt.run()
stats = bt.optimize(
    upper_bound = range(50, 85, 5),
    lower_bound = range(10, 45, 5),
    rsi_window = range(10, 30, 2),
    maximize='Sharpe Ratio',
    constraint = lambda param: param.upper_bound > param.lower_bound)

print(stats)

#launches RsiOscillator.html
bt.plot()