from requests import Session
import requests
import io
import zipfile, urllib.request, shutil
from datetime import datetime
import os
import pandas as pd
import logging
import xml.etree.ElementTree as etree
import urllib3
import csv
from utils.WebSession import old_nse_webSession,new_nse_webSession

# If Its Holiday or Weekend Dont Run the Script
#######################################################################
html_holidays = new_nse_webSession.request("GET",url="https://www.nseindia.com/products-services/equity-market-timings-holidays").text
#print(html_holidays)
holiday_data = pd.read_html(html_holidays)
holiday_date_list = holiday_data[0]["Date"].tolist()
weekno = datetime.today().weekday()
if weekno > 5 or datetime.today().date().strftime("%d-%b-%Y") in holiday_date_list:
	print("Its Holiday Today so Bye bye.....")
	exit()

#Some Variable Intialization
########################################################################
todaysDate = datetime.today().date()
currentMonth = todaysDate.strftime('%b').upper()
currentMonthNumber = todaysDate.strftime('%m')
currentYear  = todaysDate.strftime('%Y')
currentYearShort = todaysDate.strftime('%y')
currentDate = todaysDate.strftime("%d")
todaysDateFormatted = todaysDate.strftime('%d%m%Y')
currentMonthLower = todaysDate.strftime('%b')

CASH_ROOT_PATH='/home/StockData/stock_data/cash/'
FNO_ROOT_PATH="/home/StockData/stock_data/fno/"

# Logging
######################################################
log_path = os.path.join('logs',currentDate+currentMonthNumber+currentYear+"_options.log")
logging.basicConfig(filename=log_path,level=logging.DEBUG)

logging.debug("--------------------------------------------" + str(datetime.today()) +" ---------------------------------------------")

# Directory
fno_report_directory = os.path.join(FNO_ROOT_PATH,todaysDateFormatted)
if not os.path.exists(fno_report_directory):
	os.makedirs(os.path.join(fno_report_directory,'option_chain'))
if os.path.exists(fno_report_directory):
	if not os.path.exists(os.path.join(fno_report_directory,'option_chain')):
		os.mkdir(os.path.join(fno_report_directory,'option_chain'))

fno_option_path = os.path.join(fno_report_directory,'option_chain')

logging.debug("Directory '% s' created" % fno_report_directory)


#1. Get List of FNO Stocks
req = old_nse_webSession.request('GET','https://www1.nseindia.com/content/fo/fo_underlyinglist.htm').text
attribute ={'cellpadding':'4','cellspacing':'1'}
indices = ['NIFTY','NIFTYIT','BANKNIFTY']
indices_url = 'https://www.nseindia.com/api/option-chain-indices?symbol='
stock_url = 'https://www.nseindia.com/api/option-chain-equities?symbol='

fno_stock_list = pd.read_html(req,attrs=attribute)[0].drop(4)
for ind in fno_stock_list.index:
	stock_code = fno_stock_list[1][ind]
	if not stock_code == 'Symbol':
		if stock_code in indices:
			#print(stock_code)
			indice_resp = new_nse_webSession.request('GET',indices_url+stock_code).text
			stock_file = open(os.path.join(fno_option_path,stock_code+".json"),"w")
			stock_file.write(indice_resp)
			stock_file.close()
			logging.debug("Downloaded for:" + stock_code)
		else:
			file_name = stock_code
			if stock_code.find('&') != -1:
				stock_code = stock_code.replace('&', '%26')
			indice_resp = new_nse_webSession.request('GET', stock_url + stock_code).text
			stock_file = open(os.path.join(fno_option_path,file_name+".json"), "w")
			stock_file.write(indice_resp)
			stock_file.close()
			logging.debug("Downloaded for:" + stock_code)