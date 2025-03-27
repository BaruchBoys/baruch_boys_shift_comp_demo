import shift
import asyncio

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



async def close_all_positions(trader,ticker,item):
    await asyncio.sleep(0.5)
    long_shares = item.get_long_shares()
    short_shares = item.get_short_shares()
    if long_shares > 0:
        print(f"Closing long: Market selling {long_shares} shares of {ticker}")
        market_sell(trader,ticker,int(long_shares/100))

    if short_shares > 0:
        print(f"Closing short: Market buying {short_shares} shares of {ticker}")
        market_buy(trader,ticker,int(short_shares/100))
