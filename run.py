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

def main(argv):
    trader = shift.Trader(USERNAME)
    try: 
        trader.connect("initiator.cfg", PASSWORD)
        trader.sub_all_order_book()
    except shift.IncorrectPasswordError as e:
        print(e)
    except shift.ConnectionTimeoutError as e:
        print(e)


    
    ticker = "AAPL"
    bollinger_strat(trader,ticker)

    trader.disconnect()



if __name__ == "__main__":
    main(sys.argv)