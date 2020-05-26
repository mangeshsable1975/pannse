from nsepy.commons import URLFetch
from requests import Session
from functools import partial
from urllib.parse import urlparse,urlencode
import urllib
from requests.utils import requote_uri

session = Session()
# headers = {
# 'Host': 'www1.nseindia.com',
# 'Referer': 'https://www1.nseindia.com/products/content/equities/equities/eq_security.htm'}

headers = {'Accept': '*/*',
		   'Accept-Encoding': 'gzip, deflate, sdch, br',
		   'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
		   'Connection': 'keep-alive',
		   'Host': 'www1.nseindia.com',
		   'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
		   'X-Requested-With': 'XMLHttpRequest'}

URLFetchSession = partial(URLFetch, session=session,
						  headers=headers)

get_nifty_fno_url = URLFetchSession(
	url='http://www1.nseindia.com/live_market/dynaContent/live_watch/fomwatchsymbol.jsp?key=NIFTY&Fut_Opt=Futures')

get_nifty_opt_chain_url = URLFetchSession(
	url="https://www1.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp")


def get_incices_opt_chain_url(stock_code):
	nifty_opt_chain_url = URLFetchSession(
		url="https://www.nseindia.com/api/option-chain-indices?symbol=" + stock_code)
	return nifty_opt_chain_url()


def get_equities_opt_chain_url(stock_code):
	if stock_code.find('&') != -1:
			stock_code = stock_code.replace('&','%%26')

	#print(stock_code)
	nifty_opt_chain_url = URLFetchSession(url="https://www.nseindia.com/api/option-chain-equities?symbol=" + stock_code)
	return nifty_opt_chain_url()


get_option_chain_updated_date_url = URLFetchSession(
	url='https://www1.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp')

get_bhav_copy_url = URLFetchSession(url = "https://www1.nseindia.com/archives/equities/mkt/MA200520.csv")


def get_nse_holiday_list_url():
	return "https://www.nseindia.com/products-services/equity-market-timings-holidays"


def get_fno_stock_list_url():
	return "https://archives.nseindia.com/content/fo/fo_mktlots.csv"
