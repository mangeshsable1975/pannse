from config.postgres_connection import session
from model.nse_cash_daily import NseCashDaily
from model.stock_list import StockList
from datawrapper.nse_daily_cash_data_wrapper import get_history_wrapper
from datetime import date, datetime, timedelta
import pandas as pd
import time
from sqlalchemy import func, join

pd.set_option('display.max_columns', None)
todaysDate = datetime.today().date()


# Clean Cash data older than 365 days
def cleanOlderData():
    session.query(NseCashDaily).filter(NseCashDaily.trade_date < (todaysDate - timedelta(days=365))).delete()
    session.commit()


cleanOlderData()

# print("Starting Data Download from :" + str(fromDate) + " to :" + str(toDate))

start_time = time.time()
stocks = session.query(StockList)
for stock in stocks:
    print("######################## Running for Stock:" + stock.stock_code)
    if stock.cash_updated < todaysDate:
        print("START : Getting History......")
        stock_ohlc_data = get_history_wrapper(symbol=stock.stock_code, start=stock.cash_updated, end=todaysDate)
        print("END : Got History......")
        for ind in stock_ohlc_data.index:
            if stock_ohlc_data.index.values.size > 0:
                try:
                    print("START: Inserting into DB......")
                    trade_date = ind
                    # print(type(stock_ohlc_data["Volume"][ind].item()))
                    print(stock_ohlc_data["Volume"][ind].item())
                    # print(stock_ohlc_data.index.values.item())
                    nseDaily = NseCashDaily(trade_date=trade_date, stock_id=stock.stock_id,
                                            stock_code=stock_ohlc_data["Symbol"][ind],
                                            series=stock_ohlc_data["Series"][ind],
                                            prev_close=stock_ohlc_data["Prev Close"][ind],
                                            open=stock_ohlc_data["Open"][ind], high=stock_ohlc_data["High"][ind],
                                            low=stock_ohlc_data["Low"][ind], close=stock_ohlc_data["Close"][ind],
                                            volume=stock_ohlc_data["Volume"][ind].item(),
                                            vwap=stock_ohlc_data["VWAP"][ind],
                                            trades=stock_ohlc_data["Trades"][ind].item(),
                                            deliverable_volume=stock_ohlc_data["Deliverable Volume"][ind].item(),
                                            percentage_delivery=stock_ohlc_data["%Deliverble"][ind])
                    # print(nseDaily)
                    session.add(nseDaily)
                    print("END: Inserted into DB......")
                except Exception as ex:
                    print("ERROR: while Create NSEDAILY Object:")
                    print(ex)

        try:
            session.commit()
            session.query(StockList).filter(StockList.stock_code == stock.stock_code).update(
                {StockList.cash_updated: todaysDate}, synchronize_session=False)
            session.commit()
        except Exception as ex:
            print("ERROR: while Commiting Last Session Data......")
            print(ex)


#print("To download NSE all Stock Data from:" + str(fromDate) + " to :" + str(toDate))
#print("took %s seconds " % (time.time() - start_time))
