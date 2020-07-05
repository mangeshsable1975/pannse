from datetime import datetime,timedelta
import os
import pandas as pd
from datawrapper.nse_daily_cash_data_wrapper import get_history_wrapper
from utils.WebSession import old_nse_webSession,new_nse_webSession
pd.set_option('display.max_columns', None)
from retrying import retry
import win32com.client as wcl

abDatabase = 'D:\\Data\\Amibroker\\Databases\\PYTHON_NSE_DAILY'
#abFormat = 'D:\\Data\\Amibroker\\Formats\\pyImport.format'
abFormat = 'D:\\Data\\Amibroker\\Formats\\python_daily_cash_import.format'
FILE_ROOT = 'D:\\Data_Files'
AB = wcl.Dispatch( 'Broker.Application')
AB.LoadDatabase(abDatabase)

from_date = datetime.today().date()
to_date = datetime.today().date()

LATEST_SYMBOL_FILE_PATH='D:\\Data\\Latest_Trading_Symbols'
FILE_ROOT_PATH='D:\\Data_Files'
DATA_FILE_NAME = 'NSE_DAILY_CASH_DATA_' + str(to_date) + '.csv'

if not os.path.exists(os.path.join(FILE_ROOT_PATH,str(to_date))):
	os.mkdir(os.path.join(FILE_ROOT_PATH,str(to_date)))

if os.path.exists(os.path.join(FILE_ROOT_PATH,str(to_date))):
	file_headers = open(os.path.join(FILE_ROOT_PATH, str(to_date), DATA_FILE_NAME), "w")
	file_headers.write("Date,Symbol,Open,High,Low,Close,Volume,Deliverable Volume,VWAP \n")
	file_headers.close()

SOURCE_FILE = os.path.join(FILE_ROOT_PATH, str(to_date), DATA_FILE_NAME)

latest_equity_list = 'https://www1.nseindia.com/content/equities/EQUITY_L.csv'
lastest_equity_list_filename = os.path.join(LATEST_SYMBOL_FILE_PATH,'latest_equity_list.csv')
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
	stock_ohlc_data = download_historical_data(ticker,from_date,to_date)
	print("Got Data for :" + ticker)
	stock_ohlc_data.index = pd.to_datetime(stock_ohlc_data.index,format='%Y-%m-%d').strftime('%Y%m%d')
	stock_ohlc_data.drop(['Series','Prev Close','Last','Turnover','Trades','%Deliverble'],axis=1,inplace=True)
	stock_ohlc_data = stock_ohlc_data[['Symbol','Open','High','Low','Close','Volume','Deliverable Volume','VWAP']]
	print("Saving to File :" + ticker)
	stock_ohlc_data.to_csv(SOURCE_FILE,mode='a',header=False)


AB.Import(0, SOURCE_FILE, abFormat)
AB.Refreshall()
AB.SaveDatabase()

print("Data for Date:" + str(to_date) + "Loaded to Amibroker")
