from datascrapper import nse_urls
import pandas as pd
from utils.WebSession import new_nse_webSession
from datetime import datetime

def get_nse_holiday_list():
	print(nse_urls.get_nse_holiday_list_url())
	html_holidays = new_nse_webSession.request("GET",url=nse_urls.get_nse_holiday_list_url()).text
	#print(html_holidays)
	holiday_data = pd.read_html(html_holidays)
	#holiday_data[0]["Date"] = holiday_data[0]["Date"]
	date_data = holiday_data[0]["Date"].tolist()
	print(datetime(2020,4,2).date().strftime("%d-%b-%Y"))
	print(date_data)
	if datetime.date().strftime("%d-%b-%Y") in date_data:
			print("Its holiday Today")
	#return date_data

get_nse_holiday_list()