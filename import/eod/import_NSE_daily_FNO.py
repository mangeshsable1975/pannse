from config.postgres_connection import session
from model.nse_fno_daily import NseFNODaily
from nsepy import get_history
from datetime import date, timedelta, datetime
from model.stock_list import StockList
from datascrapper import nse_utils
from sqlalchemy import func

# Initilization
todaysDate = date.today()


# Clean up passed expiry data from table


def cleanupOldFnOData():
	session.query(NseFNODaily).filter(NseFNODaily.expiry_date < todaysDate).delete()
	session.commit()


cleanupOldFnOData()

# get Next 3 Expiry data for today
expiry_dates = nse_utils.findNextExpiryDatesForStocks()

# #with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
# #    print(stock_ohlc_data)
#

indices = session.query(StockList).filter(StockList.indices == True)
indices_list = [ind.stock_code for ind in indices]

stocks = session.query(StockList).filter(StockList.fno == True)

for stock in stocks:
	print("######################## Running for Stock:" + stock.stock_code)
	if stock.fno_updated < todaysDate:
		for expiry_date in expiry_dates:

			stock_ohlc_data = get_history(symbol=stock.stock_code, start=stock.fno_updated, end=todaysDate,
										  expiry_date=expiry_date,
										  futures=True, index=True if stock.stock_code in indices_list else False)
			# print(stock_ohlc_data.dtypes)
			for ind in stock_ohlc_data.index:
				if stock_ohlc_data.index.values.size > 0:
					trade_date = ind
					nseFNODaily = NseFNODaily(stock_id=stock.stock_id, trade_date=trade_date,
											  stock_code=stock_ohlc_data["Symbol"][ind], expiry_date=expiry_date,
											  open=stock_ohlc_data["Open"][ind], high=stock_ohlc_data["High"][ind],
											  low=stock_ohlc_data["Low"][ind], close=stock_ohlc_data["Close"][ind],
											  last_price=stock_ohlc_data["Last"][ind],
											  settle_price=stock_ohlc_data["Settle Price"][ind],
											  no_of_contracts=stock_ohlc_data["Number of Contracts"][ind].item(),
											  open_interest=stock_ohlc_data["Open Interest"][ind].item(),
											  change_in_oi=stock_ohlc_data["Change in OI"][ind].item(),
											  underlying=stock_ohlc_data["Underlying"][ind])
					# print(nseFNODaily)
					session.add(nseFNODaily)
				# print("END: Inserted into DB......")

			try:
				session.commit()
				session.query(StockList).filter(StockList.stock_code == stock.stock_code).update(
					{StockList.fno_updated: todaysDate}, synchronize_session=False)
				session.commit()
			except Exception as ex:
				print("Error while committing transaction...")
				print(ex)

# session.query(StockList).update({StockList.downloaded:False},synchronize_session=False)
# session.commit()

# print("Download Complete For all FNO Stock Data from:" + str(fromDate) + " to :" + str(toDate))
