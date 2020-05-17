from config.postgres_connection import session
from model.nse_cash_daily import NseCashDaily
from model.stock_list import StockList
from datawrapper.nse_daily_cash_data_wrapper import get_history_wrapper
from datetime import date
import pandas as pd
import time


pd.set_option('display.max_columns', None)

fromDate = date(2020,1,1)
toDate = date(2020,5,8)

#print("Starting Data Download from :" + fromDate + "to :" + toDate)

start_time = time.time()
stocks = session.query(StockList).filter(StockList.downloaded == False)
for stock in stocks:
    print("######################## Running for Stock:" + stock.stock_code)

    print("START : Getting History......")
    stock_ohlc_data = get_history_wrapper(symbol=stock.stock_code, start=fromDate, end=toDate)
    print("END : Got History......")
    for ind in stock_ohlc_data.index:
        if stock_ohlc_data.index.values.size > 0:
            try:
                print("START: Inserting into DB......")
                trade_date = ind
                #print(type(stock_ohlc_data["Volume"][ind].item()))
                print(stock_ohlc_data["Volume"][ind].item())
                #print(stock_ohlc_data.index.values.item())
                nseDaily = NseCashDaily(trade_date=trade_date, stock_id=stock.stock_id, stock_code=stock_ohlc_data["Symbol"][ind], series=stock_ohlc_data["Series"][ind], prev_close=stock_ohlc_data["Prev Close"][ind], open=stock_ohlc_data["Open"][ind], high=stock_ohlc_data["High"][ind], low=stock_ohlc_data["Low"][ind], close=stock_ohlc_data["Close"][ind], volume=stock_ohlc_data["Volume"][ind].item(), vwap=stock_ohlc_data["VWAP"][ind], trades=stock_ohlc_data["Trades"][ind].item(), deliverable_volume=stock_ohlc_data["Deliverable Volume"][ind].item(), percentage_delivery=stock_ohlc_data["%Deliverble"][ind])
                #print(nseDaily)
                session.add(nseDaily)
                print("END: Inserted into DB......")
            except Exception as ex:
                print("ERROR: while Create NSEDAILY Object:")
                print(ex)

    try:
        session.commit()
        stocktoupdate = session.query(StockList).filter(StockList.stock_code == stock.stock_code).update({StockList.downloaded:True},synchronize_session = False)
        #stocktoupdate.downloaed = True
        print("Updating Downloaded Flag....")
        print(stocktoupdate)
        session.commit()
    except Exception as ex:
        print("ERROR: while Commiting Last Session Data......")
        print(ex)


session.query(StockList).update({StockList.downloaded:False},synchronize_session=False)
session.commit()

print("To download NSE all Stock Data from:" + str(fromDate) + " to :" + str(toDate))
print("took %s seconds " % (time.time() - start_time))
