
from datetime import datetime,timedelta
import datetime as dt
import numpy as np
from utils.order_utils import *
from utils.portfolio_utils import *

def bollinger_strat(trader,ticker):
    # Sampling session
    trader.request_sample_prices([ticker],sampling_frequency=1.0,sampling_window=21)
    sleep(23)

    #Trading Session 
    start_time = trader.get_last_trade_time()
    end_time = start_time + timedelta(hours=5)

    #Main Loop 
    while trader.get_last_trade_time() < end_time:
        sample_prices = trader.get_sample_prices(ticker)
        if len(sample_prices) >= 20:
            sma = np.mean(sample_prices[-20:])
            std = np.std(sample_prices[-20:])
            upper_band = sma + (2*std)
            lower_band = sma - (2*std) 

            last_price = get_last_price(trader,ticker)

            if last_price > upper_band:
                #sell signal 
                limit_sell(trader,ticker,1,last_price)
            elif last_price < lower_band:
                #buy signal 
                limit_buy(trader,ticker,1,last_price)
        sleep(1)

     # Closing all positions after trading window    
    close_all_positions(trader,ticker)
    