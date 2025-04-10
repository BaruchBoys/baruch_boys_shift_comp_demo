import shift
import asyncio
from datetime import datetime, timedelta
from utils.credentials import USERNAME, PASSWORD
from utils.order_utils import *
from utils.portfolio_utils import *
from stratergies.pickens_method import *
from time import sleep


async def close_positions(trader,ticker):
    await asyncio.sleep(0.5)
    item = trader.get_portfolio_item(ticker)
    await close_all_positions(trader, ticker, item)

async def process_ticker(trader:shift.Trader, ticker:str, data:dict, upper_bound:float,lower_bound:float,order_table:list):
    try:
        print(f"Processing ticker: {ticker}")
        item = trader.get_portfolio_item(ticker)
        long_shares = item.get_long_shares()
        short_shares = item.get_short_shares()
        threshold = 100
        await asyncio.sleep(0.5)
        print(f"{ticker} has {short_shares} short shares and {long_shares} long shares:")


        p_fluc = data["p_fluc"]
        last = data["last_price"]
        first = data["first_price"]

        bp = trader.get_best_price(ticker)
        spread = abs((last - first) / last) if last != 0 else 0

        ask_price = bp.get_ask_price() + spread
        bid_price = bp.get_bid_price() - spread

        position_size = 1
        if lower_bound <= p_fluc <= upper_bound:
            print(f"{ticker} fluctuation: {p_fluc:.2f}, placing limit orders")
            if ask_price > bid_price:
                order_sell = await limit_sell(trader, ticker, position_size,ask_price)
                order_buy = await limit_buy(trader, ticker, position_size,bid_price)
                order_table.append(order_sell)
                order_table.append(order_buy)
            return

        if long_shares >= threshold:
            await close_all_limit_positions(trader, ticker,item,ask_price)
            return
        elif short_shares >= threshold:
            await close_all_limit_positions(trader, ticker,item,bid_price)
            return


    except Exception as e:
        print(f"error happend in ticker raised exception as {e}")
    

async def main():
    trader = shift.Trader(USERNAME)
    try:
        trader.connect("initiator.cfg", PASSWORD)
        trader.sub_all_order_book()
    except shift.IncorrectPasswordError as e:
        print(e)
        return
    except shift.ConnectionTimeoutError as e:
        print(e)
        return

    tickers_list = trader.get_stock_list()
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=30)
    upper_bound = 6
    lower_bound = 5
    loop_count = 0
    order_table = []
    while trader.get_portfolio_summary().get_total_shares() < 20000:
        loop_count+=1
        print(f"Loop {loop_count} started at {datetime.now().strftime('%H:%M:%S')}")
        pickens_dict = await fetching_pickens_data(trader, tickers_list)
        print(f"Fetched Pickens data at {datetime.now().strftime('%H:%M:%S')}")

        tasks = [
            process_ticker(trader, ticker, pickens_dict[ticker],upper_bound,lower_bound,order_table)
            for ticker in pickens_dict
        ]
        await asyncio.gather(*tasks)

        for order in order_table:
            trader.submit_cancellation(order)


        order_table.clear()
        print("All pending orders cancelled.\n")

   

    close_out_tasks = [close_positions(trader, ticker) for ticker in tickers_list]
    await asyncio.gather(*close_out_tasks)


    trader.disconnect()
    print("Session complete. Disconnected.")


if __name__ == "__main__":
    asyncio.run(main())
