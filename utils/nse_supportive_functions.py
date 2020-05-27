from datascrapper import nse_urls
import pandas as pd
from utils.WebSession import new_nse_webSession
from datetime import datetime,timedelta


def get_nse_holiday_list():
	print(nse_urls.get_nse_holiday_list_url())
	html_holidays = new_nse_webSession.request("GET",url=nse_urls.get_nse_holiday_list_url()).text
	#print(html_holidays)
	holiday_data = pd.read_html(html_holidays)
	#holiday_data[0]["Date"] = holiday_data[0]["Date"]
	holiday_list = holiday_data[0]["Date"].tolist()
	return holiday_list


def get_working_days(d, end, excluded=(6, 7)):
	days = []
	while d.date() <= end.date():
		if d.isoweekday() not in excluded:
			days.append(d)
		d += timedelta(days=1)
	return days
