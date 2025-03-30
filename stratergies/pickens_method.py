import asyncio
import shift


tickers_dict = {}
async def fetch_data(trader: shift.Trader, ticker): 
    global tickers_dict  
    tickers_dict.clear()
    ticker_price = []
    max_tries = 10
    tries = 0
    while tries <= max_tries: 
        current_price = trader.get_last_price(ticker)

        if current_price == 0.0 or current_price in ticker_price: 
             tries += 1
             await asyncio.sleep(0.5) 
             continue
        
        ticker_price.append(current_price)

        if len(ticker_price)  == 2:  
            first, last = ticker_price[0], ticker_price[1]
            p_fluc_t = abs((last - first) / last) * 10000
            tickers_dict[ticker] = {
                "first_price": first,
                "last_price": last,
                "p_fluc": p_fluc_t
            }
            break   
        


async def fetching_pickens_data(trader: shift.Trader,tickers_list):
    # print("Starting tasks for:", tickers_list)

    tasks = []
    for ticker in tickers_list:
        tasks.append(fetch_data(trader, ticker))

    await asyncio.gather(*tasks)  

    
    return tickers_dict

