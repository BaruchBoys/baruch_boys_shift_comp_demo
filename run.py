import shift
import sys
import os
from utils.credentials import USERNAME, PASSWORD
from utils.order_utils import *
from utils.portfolio_utils import *
from stratergies.bollinger_bands import *
from stratergies.pickens_method import *
import json
import time
from random import choice

async def pickens_process(trader: shift.Trader, ticker):
    pass


def main(argv):
    trader = shift.Trader(USERNAME)
    try: 
        trader.connect("initiator.cfg", PASSWORD)
        trader.sub_all_order_book()
    except shift.IncorrectPasswordError as e:
        print(e)
    except shift.ConnectionTimeoutError as e:
        print(e)
    tickers_list = trader.get_stock_list()

    start_time = datetime.now()
    end_time = datetime.now() + dt.timedelta(hours=6.5)

    h = 3
    orders = 0
    while datetime.now() < end_time: 
        pickens_dict = asyncio.run(fetching_pickens_data(trader,tickers_list))
        for ticker in pickens_dict.keys():
            item = trader.get_portfolio_item(ticker)
            if item.get_shares() > 200: 
                close_all_positions(trader,ticker)

            p_fluc = pickens_dict[ticker]["p_fluc"]
            last = pickens_dict[ticker]["last_price"]
            first = pickens_dict[ticker]["first_price"]
            bp = trader.get_best_price(ticker)
            if p_fluc > h: 
                if bp.get_ask_price() + abs(( last - first)/last ) > bp.get_bid_price() - abs(( last - first)/last ):
                    limit_sell(trader,ticker,1,bp.get_ask_price() + abs(( last - first)/last ))
                    limit_buy(trader,ticker,1,bp.get_bid_price() - abs(( last - first)/last ))
                    orders += 2
                    print(f"submitting total orders {orders} currently submitting order for {ticker}")
                else:
                    continue
        trader.cancel_all_pending_orders()
    

    trader.disconnect()


   



if __name__ == "__main__":
    main(sys.argv)