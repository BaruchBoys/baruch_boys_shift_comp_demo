import shift
import sys
import os
from datetime import datetime,timedelta
import datetime as dt
import numpy as np
from utils.credentials import USERNAME, PASSWORD
from utils.order_utils import *
from utils.portfolio_utils import *
from stratergies.bollinger_bands import bollinger_strat
import asyncio

def main(argv):
    trader = shift.Trader(USERNAME)
    try: 
        trader.connect("initiator.cfg", PASSWORD)
        trader.sub_all_order_book()
    except shift.IncorrectPasswordError as e:
        print(e)
    except shift.ConnectionTimeoutError as e:
        print(e)


    start_time = trader.get_last_trade_time()
    end_time = start_time + timedelta(seconds=30)

    ticker = "AAPL"
    sma = asyncio.run(get_sma(trader,ticker,1.0,20))
    print(get_last_price())
    print(sma)
    
    trader.disconnect()



if __name__ == "__main__":
    main(sys.argv)