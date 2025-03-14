import shift 
import sys
import time 
from time import sleep 
from random import uniform
from datetime import datetime, timedelta
import datetime as dt 


def port_summary(trader: shift.Trader):
    """
    This method provides information on the structure of PortfolioSummary and PortfolioItem objects:
     get_portfolio_summary() returns a PortfolioSummary object with the following data:
     1. Total Buying Power (get_total_bp())
     2. Total Shares (get_total_shares())
     3. Total Realized Profit/Loss (get_total_realized_pl())
     4. Timestamp of Last Update (get_timestamp())

     get_portfolio_items() returns a dictionary with "symbol" as keys and PortfolioItem as values,
     with each providing the following information:
     1. Symbol (get_symbol())
     2. Shares (get_shares())
     3. Price (get_price())
     4. Realized Profit/Loss (get_realized_pl())
     5. Timestamp of Last Update (get_timestamp())
    :param trader:
    :return:
    """

    print("Buying Power\tTotal Shares\tTotal P&L\tTimestamp")
    print(
        "%12.2f\t%12d\t%9.2f\t%26s"
        % (
            trader.get_portfolio_summary().get_total_bp(),
            trader.get_portfolio_summary().get_total_shares(),
            trader.get_portfolio_summary().get_total_realized_pl(),
            trader.get_portfolio_summary().get_timestamp(),
        )
    )

    print()

    print("Symbol\t\tShares\t\tPrice\t\t  P&L\tTimestamp")
    for item in trader.get_portfolio_items().values():
        print(
            "%6s\t\t%6d\t%9.2f\t%9.2f\t%26s"
            % (
                item.get_symbol(),
                item.get_shares(),
                item.get_price(),
                item.get_realized_pl(),
                item.get_timestamp(),
            )
        )
    return
def market_buy(trader: shift.Trader,ticker,pos_size):
    order = shift.Order(shift.Order.Type.MARKET_BUY,ticker,pos_size)
    trader.submit_order(order)

def market_sell(trader: shift.Trader,ticker,pos_size):
    order = shift.Order(shift.Order.Type.MARKET_SELL,ticker,pos_size)
    trader.submit_order(order)

def limit_buy(trader: shift.Trader,ticker,pos_size,price):
    order = shift.Order(shift.Order.Type.LIMIT_BUY,ticker,pos_size,price)
    trader.submit_order(order)

def limit_sell(trader: shift.Trader,ticker,pos_size,price):
    order = shift.Order(shift.Order.Type.LIMIT_SELL,ticker,pos_size,price)
    trader.submit_order(order)

def get_price(trader: shift.Trader,ticker):
    return trader.get_last_price(ticker)





def strat(trader,ticker):
    limit_buy(trader,ticker,1,uniform(get_price(trader,ticker) + 3, get_price(trader,ticker) - 3))
    limit_sell(trader,ticker,1,uniform(get_price(trader,ticker) + 3, get_price(trader,ticker) - 3))

def close_positions(trader: shift.Trader,ticker): 
    print(f"running close positions functions for {ticker}")
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
    



def main(argv):
    trader = shift.Trader("democlient")
    try:
        trader.connect("initiator.cfg", "password")
        trader.sub_all_order_book()
    except shift.IncorrectPasswordError as e:
        print(e)
    except shift.ConnectionTimeoutError as e:
        print(e)

    sleep(20)
    for i in range(100):
        print(trader.get_last_price("MSFT"))
        strat(trader,"AAPL")

    sleep(10)
    close_positions(trader,"AAPL")
    # port_summary(trader)

    trader.disconnect()

    return

if __name__ == "__main__":
    main(sys.argv)