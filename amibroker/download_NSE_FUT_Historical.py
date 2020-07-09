import io
import zipfile
from datetime import datetime,timedelta
import os
import pandas as pd
from datawrapper.nse_daily_cash_data_wrapper import get_history_wrapper
from utils.WebSession import old_nse_webSession,new_nse_webSession
from nsepy import get_history
from retrying import retry
from datascrapper import nse_utils
from nsepy.derivatives import get_expiry_date
import calendar
import itertools

pd.set_option('display.max_columns', None)

from_date = datetime(2020,1,1).date()
to_date = datetime.today().date()
history_period = 90 # How may days back data needed

DAILY_FUT_PRICE='D:\\Data_Files\\FUTURE'


#@retry(wait_fixed=5000)
def download_future_data(ticker, start_date, end_date,expiry,is_index):
	stock_fut_data = get_history(symbol=ticker, start=start_date, end=end_date,
									expiry_date=expiry,futures=True, index=is_index)
	return stock_fut_data


expiry_dates = nse_utils.findNextExpiryDatesForStocks()
# expiry_dates = get_expiry_date(year=datetime.today().year, month=datetime.today().month)
# next_month = calendar.nextmonth(datetime.today().year,month=datetime.today().month)
# print(type(next_month))
# next_expiry_dates = get_expiry_date(year=next_month[0], month=next_month[1])
# print(next_expiry_dates)

#1. Get List of FNO Stocks
req = old_nse_webSession.request('GET','https://www1.nseindia.com/content/fo/fo_underlyinglist.htm').text
attribute ={'cellpadding':'4','cellspacing':'1'}
indices = ['NIFTY','NIFTYIT','BANKNIFTY']

fno_stock_list = pd.read_html(req,attrs=attribute)[0].drop(4)
#fno_stock_list = fno_stock_list.iloc[2:]
print(fno_stock_list.columns.tolist())
filter_stock_list = ['Derivatives on Individual Securities','Derivatives on Individual Securities','Symbol']
file_headers = 'Date,Symbol,Expiry,Open,High,Low,Close,Last,Settle Price,Number Of Contracts,Turnover,Open Interest,Change in OI,Underlying\n'
# def nearest_expiry(items, pivot):
# 	return min(items, key=lambda x: abs(x - pivot))


def get_all_expirty_date_within_range(from_date,to_date):
	num_months = (to_date.year - from_date.year) * 12 + (to_date.month - from_date.month) + 2
	current_date = from_date
	monthly_expiries = []
	for month in range(0,num_months):
		monthly_expiries.append(get_expiry_date(current_date.year,current_date.month,False,True))
		next_month = calendar.nextmonth(current_date.year,current_date.month)
		current_date = datetime(next_month[0],next_month[1],1).date()

	flttern_monthly_expiries = list(itertools.chain.from_iterable(monthly_expiries))
	return flttern_monthly_expiries


monthly_expiries = get_all_expirty_date_within_range(from_date,to_date)

for ind in fno_stock_list.index:
	stock_code = fno_stock_list[1][ind]
	#print("Started for :" + stock_code)
	#master_df = pd.DataFrame()
	#print(filter_stock_list)
	print(stock_code)
	if stock_code not in filter_stock_list:
		print("Started for :" + stock_code)
		# Add Headers to File
		DATA_FILE_NAME = stock_code + "_" + str(from_date) + "_" + str(to_date) + ".csv"
		file_handle = open(os.path.join(DAILY_FUT_PRICE, DATA_FILE_NAME), 'w')
		file_handle.write(file_headers)
		file_handle.close()
		reset_from_date = from_date
		total_expiry_count = len(monthly_expiries)
		#print("Total Expiries:" + str(total_expiry_count))

		for expiry in range(0,total_expiry_count):
			is_indices = stock_code in indices
			#print("Current Index:" + str(index_expiry))
			current_month_expiry_date = monthly_expiries[expiry]
			#print("From Date:" + str(from_date) + ",To Date:" + str(current_month_expiry_date))
			current_month_expiry_data = download_future_data(stock_code,reset_from_date,current_month_expiry_date, current_month_expiry_date, is_indices)
			#print("################################################")
			#print(current_month_expiry_data.head())
			#print("################################################")

			#print(current_week_expiry_data.head())
			if total_expiry_count > expiry + 1:
				far_month_expiry_date = monthly_expiries[expiry + 1]
				far_month_expiry_data = download_future_data(stock_code,from_date,current_month_expiry_date,
															far_month_expiry_date, is_indices)
				current_month_expiry_data['Open Interest'] = current_month_expiry_data['Open Interest'] + \
															far_month_expiry_data['Open Interest']
				current_month_expiry_data['Change in OI'] = current_month_expiry_data['Change in OI'] + \
															far_month_expiry_data['Change in OI']

			if total_expiry_count > expiry + 2:
				farther_month_expiry_date = monthly_expiries[expiry + 2]
				farther_month_expiry_data = download_future_data(stock_code, from_date, current_month_expiry_date,
																far_month_expiry_date, is_indices)
				current_month_expiry_data['Open Interest'] = current_month_expiry_data['Open Interest'] + \
															farther_month_expiry_data['Open Interest']
				current_month_expiry_data['Change in OI'] = current_month_expiry_data['Change in OI'] + \
														   farther_month_expiry_data['Change in OI']

			current_month_expiry_data.to_csv(os.path.join(DAILY_FUT_PRICE, DATA_FILE_NAME), mode='a', header=False)
			reset_from_date = current_month_expiry_date + timedelta(days=1)

	# else:
	# 	if not stock_code == 'Symbol' and stock_code == 'NIFTY':
	# 		if stock_code in indices:
	# 			next_2_months_expiries = get_next_2_months_expiry(True, single_date)
	# 			print(next_2_months_expiries)
	# 			next_expiry = nearest_expiry(next_2_months_expiries,single_date)
	# 			print(next_expiry)
	# 			to_date = next_expiry
	# 			for expiry_date in next_2_months_expiries:
	# 				if single_date > expiry_date:
	# 					from_date = single_date
	# 				if expiry_date == next_expiry:
	# 					print("Closed Expiry :" + str(expiry_date))
	# 					master_df = download_future_data(stock_code, from_date, to_date, expiry_date,True)
	# 					print(master_df.head())
	# 				else:
	# 					print("Far Expiry :" + str(expiry_date))
	# 					far_expiry_data = download_future_data(stock_code, from_date, to_date, expiry_date,True)
	# 					master_df['Open Interest'] = master_df['Open Interest'] + far_expiry_data['Open Interest']
	# 					master_df['Change in OI'] = master_df['Change in OI'] + far_expiry_data['Change in OI']
	# 					print(master_df.head())
	# 		else:
	# 			next_2_months_expiries = get_next_2_months_expiry(True,single_date)
	# 			next_expiry = nearest_expiry(next_2_months_expiries, single_date)
	# 			for expiry_date in next_2_months_expiries:
	# 				if expiry_date == next_expiry:
	# 					print("Closed Expiry :" + str(expiry_date))
	# 					master_df = download_future_data(stock_code,from_date,to_date,expiry_date,False)
	# 				else:
	# 					far_expiry_data = download_future_data(stock_code, from_date, to_date, expiry_date,False)
	# 					master_df['Open Interest'] = master_df['Open Interest'] + far_expiry_data['Open Interest']
	# 					master_df['Change in OI'] = master_df['Change in OI'] + far_expiry_data['Change in OI']
	#
	# 		master_df.to_csv(os.path.join(DAILY_FUT_PRICE, DATA_FILE_NAME),mode='a')
	# 	#print(master_df.head())

