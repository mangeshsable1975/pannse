from config.postgres_connection import session
from model.nse_cash_daily import NseCashDaily
from model.stock_list import StockList
from datawrapper.nse_daily_cash_data_wrapper import get_history_wrapper
from datetime import date
import pandas as pd
import time
import os
import win32com.client as wcl
from nsepy.history import get_price_list
pd.set_option("display.width",1500)
pd.set_option("display.max_columns",75)
pd.set_option("display.max_rows",1500)

abDatabase = 'D:\\Data\\Amibroker\\Databases\\PYTHON_NSE_DAILY'
#abFormat = 'D:\\Data\\Amibroker\\Formats\\pyImport.format'
abFormat = 'D:\\Data\\Amibroker\\Formats\\python_daily_cash_import.format'
FILE_ROOT = 'D:\\Data_Files'
AB = wcl.Dispatch( 'Broker.Application')
AB.LoadDatabase(abDatabase)

pd.set_option('display.max_columns', None)
for root, dirs, files in os.walk(FILE_ROOT):
	for file in files:
		#if 'CIPLA' in file:
			file_handle = os.path.join(root,file)
			print("Loading....." + file_handle)
			AB.Import(0, file_handle, abFormat)
			time.sleep(60)
			AB.Refreshall()
			AB.SaveDatabase()

AB.Refreshall()
AB.SaveDatabase()
