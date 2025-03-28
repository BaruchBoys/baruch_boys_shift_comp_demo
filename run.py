import shift
import asyncio
from datetime import datetime, timedelta
from utils.credentials import USERNAME, PASSWORD
from utils.order_utils import *
from utils.portfolio_utils import *
from stratergies.bollinger_bands import *
from stratergies.pickens_method import *
from random import choice


async def close_positions(trader,ticker):
    await asyncio.sleep(0.5)
    item = trader.get_portfolio_item(ticker)
    await close_all_positions(trader, ticker, item)

async def process_ticker(trader, ticker, data, h):
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

    
    if not (5 <= p_fluc <= h):
        print(f"{ticker} skipped: fluctuation {p_fluc:.2f} ≤ threshold {h}")
        return
    print(f"{ticker} fluctuation: {p_fluc:.2f}, placing limit orders")

    bp = trader.get_best_price(ticker)
    spread = abs((last - first) / last) if last != 0 else 0

    ask_price = bp.get_ask_price() + spread
    bid_price = bp.get_bid_price() - spread
    if long_shares >= threshold:
        await close_all_limit_positions(trader, ticker,item,ask_price,"sell")
        return
    elif short_shares >= threshold:
        await close_all_limit_positions(trader, ticker,item,bid_price,"buy")
        return





    position_size = 3
    if ask_price > bid_price:
        limit_sell(trader, ticker, position_size, ask_price)
        limit_buy(trader, ticker, position_size, bid_price)

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

    print("Starting trading session...")
    tickers_list = trader.get_stock_list()

    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=30)
    h = 7
    loop_count = 0
    while datetime.now() < end_time:
        loop_count+=1
        print(f"Loop {loop_count} started at {datetime.now().strftime('%H:%M:%S')}")

        pickens_dict = await fetching_pickens_data(trader, tickers_list)
        print(f"Fetched Pickens data at {datetime.now().strftime('%H:%M:%S')}")

        tasks = [
            process_ticker(trader, ticker, pickens_dict[ticker], h)
            for ticker in pickens_dict
        ]
        await asyncio.gather(*tasks)
        trader.cancel_all_pending_orders(10)
        print("All pending orders cancelled.\n")

    close_out_tasks = [close_positions(trader,ticker) for ticker in tickers_list]
    await asyncio.gather(*close_out_tasks)
    trader.disconnect()
    print("Session complete. Disconnected.")


if __name__ == "__main__":
    asyncio.run(main())
