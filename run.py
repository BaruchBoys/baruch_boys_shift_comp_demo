import shift
import sys
import os
import asyncio
from datetime import datetime, timedelta
from time import sleep
from utils.credentials import USERNAME, PASSWORD
from utils.order_utils import *
from utils.portfolio_utils import *
from stratergies.bollinger_bands import *
from stratergies.pickens_method import *
from random import choice


def main(argv):
    trader = shift.Trader(USERNAME)
    try: 
        trader.connect("initiator.cfg", PASSWORD)
        trader.sub_all_order_book()
    except shift.IncorrectPasswordError as e:
        print(e)
    except shift.ConnectionTimeoutError as e:
        print(e)

    print("Starting trading session...")
    tickers_list = trader.get_stock_list()

    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=1)
    h = 3

    while datetime.now() < end_time: 
        print(f"Time now: {datetime.now()}, End time: {end_time}")  # Debug: Check loop condition

        pickens_dict = asyncio.run(fetching_pickens_data(trader, tickers_list))
        
        for ticker in pickens_dict:
            item = trader.get_portfolio_item(ticker)
            shares = item.get_shares()
            print(f"You own {shares} shares of {ticker}")
            sleep(0.25)

            # Step 1: Close positions if too large
            if shares > 200:
                print(f"Closing position for {ticker}")
                close_all_positions(trader, ticker)
                continue  

            # Step 2: Trading logic
            p_fluc = pickens_dict[ticker]["p_fluc"]
            last = pickens_dict[ticker]["last_price"]
            first = pickens_dict[ticker]["first_price"]

            if p_fluc <= h:
                continue

            bp = trader.get_best_price(ticker)
            spread = abs((last - first) / last)

            ask_price = bp.get_ask_price() + spread
            bid_price = bp.get_bid_price() - spread

            if ask_price > bid_price:
                limit_sell(trader, ticker, 1, ask_price)
                limit_buy(trader, ticker, 1, bid_price)

        # Cancel all orders immediately if they don't fill
        trader.cancel_all_pending_orders()

    # Final cleanup
    for ticker in tickers_list:
        close_all_positions(trader, ticker)
    trader.disconnect()

if __name__ == "__main__":
    main(sys.argv)
