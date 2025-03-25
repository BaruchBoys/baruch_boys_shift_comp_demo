import shift
from time import sleep 
import asyncio

import numpy as np

def market_buy(trader: shift.Trader,ticker:str,position: int): # Market Buy 
    order = shift.Order(shift.Order.Type.MARKET_BUY, ticker, position)
    trader.submit_order(order)

def market_sell(trader: shift.Trader,ticker:str,position: int): # Market Sell
    order = shift.Order(shift.Order.Type.MARKET_SELL,ticker,position)
    trader.submit_order(order)

def limit_buy(trader: shift.Trader,ticker:str,position:int,price:float): # Limit Buy
    order = shift.Order(shift.Order.Type.LIMIT_BUY,ticker,position,price)
    trader.submit_order(order)

def limit_sell(trader: shift.Trader,ticker:str,position:int,price:float): # Limit Buy
    order = shift.Order(shift.Order.Type.LIMIT_SELL,ticker,position,price)
    trader.submit_order(order)

def get_last_price(trader: shift.Trader,ticker): # returns the last traded price 
    return trader.get_last_price(ticker)

def cancel_bid(trader: shift.Trader,ticker:str,position:int,price:float): # cancels bid 
    print(f"cancelling bid for {ticker} at price {price} and position {position}")
    order = shift.Order(shift.Order.Type.CANCEL_BID,ticker,position,price)
    print(order in trader.get_waiting_list())
    trader.submit_cancellation(order)


def close_all_positions(trader: shift.Trader,ticker:str): # closes all open positions for a ticker
    total_shares_of_ticker = trader.get_portfolio_item(ticker)
    long_shares = total_shares_of_ticker.get_long_shares()
    short_shares = total_shares_of_ticker.get_short_shares()

    if long_shares > 0: 
        print(f"market selling {ticker}: amount of {long_shares} long shares ")
        order = shift.Order(shift.Order.Type.MARKET_SELL,ticker,int(long_shares/100))
        trader.submit_order(order)
        sleep(1)
    
    if short_shares > 0:
        print(f"market selling {ticker}: amount of {long_shares} long shares ")
        order = shift.Order(shift.Order.Type.MARKET_SELL,ticker,int(long_shares/100))
        trader.submit_order(order)
        sleep(1)

async def get_sma(trader: shift.Trader,ticker:str,freq:float,window:int): # returns the simple moving average of a ticker 
    trader.request_sample_prices([ticker],sampling_frequency=freq,sampling_window=window)
    print("waiting for data....")
    await asyncio.sleep(freq*window)
    prices = trader.get_sample_prices(ticker)
    sma = np.mean(prices)
    return sma