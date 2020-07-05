import io
import zipfile
from datetime import datetime,timedelta
import os
import pandas as pd
from datawrapper.nse_daily_cash_data_wrapper import get_history_wrapper
from utils.WebSession import old_nse_webSession,new_nse_webSession
pd.set_option('display.max_columns', None)
from retrying import retry

fromDate = datetime.today().date() - timedelta(days=3650)
toDate = datetime.today().date() - timedelta(days=1)

def download_csv_file(web_session,url,dest_file_name):
	req = web_session.request('GET',url)
	url_content = req.content
	csv_file = open(dest_file_name, 'wb')
	csv_file.write(url_content)
	csv_file.close()

ROOT_PATH='D:\\Data\\Latest_Trading_Symbols'
DAILY_CASH_PRICE='D:\\Data_Files'

latest_equity_list = 'https://www1.nseindia.com/content/equities/EQUITY_L.csv'
lastest_equity_list_filename = os.path.join(ROOT_PATH,'latest_equity_list.csv')
#download_csv_file(old_nse_webSession,latest_equity_list,lastest_equity_list_filename)

equity_list_df = pd.read_csv(lastest_equity_list_filename)
#equity_list_df.reset_index(inplace=True)
eq_list_df = equity_list_df[equity_list_df[' SERIES'] == 'EQ']


@retry(wait_fixed=5000)
def download_historical_data(ticker, startdate, enddate):
	stock_ohlc_data = get_history_wrapper(symbol=ticker, start=startdate, end=enddate)
	return stock_ohlc_data


for ind in eq_list_df.index:
	ticker = eq_list_df['SYMBOL'][ind]
	print("Loading.... :" + ticker)
	#stock_ohlc_data = get_history_wrapper(symbol=ticker, start=fromDate, end=toDate)
	stock_ohlc_data = download_historical_data(ticker,fromDate,toDate)
	print("Got Data for :" + ticker)
	stock_ohlc_data.index = pd.to_datetime(stock_ohlc_data.index,format='%Y-%m-%d').strftime('%Y%m%d')
	stock_ohlc_data.drop(['Series','Prev Close','Last','Turnover','Trades','%Deliverble'],axis=1,inplace=True)
	stock_ohlc_data = stock_ohlc_data[['Symbol','Open','High','Low','Close','Volume','Deliverable Volume','VWAP']]
	print("Saving to File :" + ticker)
	stock_ohlc_data.to_csv(os.path.join(DAILY_CASH_PRICE,ticker +'_' + str(fromDate) + '_' + str(toDate) + '.csv'))


