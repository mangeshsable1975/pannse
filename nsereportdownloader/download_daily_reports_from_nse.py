from requests import Session
import requests
import io
import zipfile, urllib.request, shutil
from datetime import datetime
import os
import pandas as pd
import logging
import xml.etree.ElementTree as etree

# Get Web Sessions
########################################################################
old_nse_headers = {'Accept': '*/*',
		   'Accept-Encoding': 'gzip, deflate, sdch, br',
		   'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
		   'Connection': 'keep-alive',
		   'Host': 'www1.nseindia.com',
		   'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
		   'X-Requested-With': 'XMLHttpRequest'}

old_nse_webSession = requests.Session()
old_nse_webSession.headers.update(old_nse_headers)

new_nse_headers = {'Accept': '*/*',
		   'Accept-Encoding': 'gzip, deflate, sdch, br',
		   'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
		   'Connection': 'keep-alive',
		   'Host': 'www.nseindia.com',
		   'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
		   'X-Requested-With': 'XMLHttpRequest'}


new_nse_webSession = requests.Session()
new_nse_webSession.headers.update(new_nse_headers)

# If Its Holiday or Weekend Dont Run the Script
#######################################################################
html_holidays = new_nse_webSession.request("GET",url="https://www.nseindia.com/products-services/equity-market-timings-holidays").text
#print(html_holidays)
holiday_data = pd.read_html(html_holidays)
holiday_date_list = holiday_data[0]["Date"].tolist()
weekno = datetime.today().weekday()
weekno = 6
if weekno > 5 or datetime.date().strftime("%d-%b-%Y") in holiday_date_list:
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
log_path = os.path.join('logs',currentDate+currentMonthNumber+currentYear+".log")
logging.basicConfig(filename=log_path,level=logging.DEBUG)

logging.debug("--------------------------------------------" + str(datetime.today()) +" ---------------------------------------------")


def download_zip_file(web_session,url,dest_directory):
	r = web_session.request('GET', url, stream=True)
	check = zipfile.is_zipfile(io.BytesIO(r.content))
	while not check:
		r = web_session.request('GET', url, stream=True)
		check = zipfile.is_zipfile(io.BytesIO(r.content))
	else:
		z = zipfile.ZipFile(io.BytesIO(r.content))
		z.extractall(dest_directory)
	logging.debug("Zip File Download Complete.......")


def download_csv_file(web_session,url,dest_file_name):
	req = web_session.request('GET',url)
	url_content = req.content
	csv_file = open(dest_file_name, 'wb')
	csv_file.write(url_content)
	csv_file.close()
	logging.debug("CSV File Downloaded.......")



#Get Holdays List
########################################################################
#print(nse_urls.get_nse_holiday_list_url())
########################################################################

# If today is Holiday or Weekend than terminate script
########################################################################


# Create Today's Date Directory in respsective path
cash_report_directory = os.path.join(CASH_ROOT_PATH, todaysDateFormatted)
if not os.path.exists(cash_report_directory):
	os.mkdir(cash_report_directory)

logging.debug("Directory '% s' created" % cash_report_directory)

fno_report_directory = os.path.join(FNO_ROOT_PATH,todaysDateFormatted)
if not os.path.exists(fno_report_directory):
	os.mkdir(fno_report_directory)

logging.debug("Directory '% s' created" % fno_report_directory)


####################################################### CASH ############################################

#1. Get Todays BhavCopy Date
###################################################################
#File Name sample:cm22MAY2020bhav.csv.zip
#bhavCopyFileName = "cm22MAY2020bhav.csv.zip"
bhavCopyFileName = "cm" + currentDate + currentMonth + currentYear+"bhav.csv.zip"
bhavCopyUrl = "https://www1.nseindia.com/content/historical/EQUITIES/" + currentYear + "/" + currentMonth +"/" + bhavCopyFileName

logging.debug("Downloading :" + bhavCopyUrl)

download_zip_file(old_nse_webSession,bhavCopyUrl,cash_report_directory)
###############################################################################

#2. Get Market Activity Reports
######################################################################
market_activity_filename = "MA" + currentDate + currentMonthNumber + currentYearShort + ".csv"
ma_dest_file = os.path.join(cash_report_directory,market_activity_filename)
maUrl = "https://www1.nseindia.com/archives/equities/mkt/" + market_activity_filename
download_csv_file(old_nse_webSession,maUrl,ma_dest_file)
######################################################

#3. Download Daily Volatility
#######################################################################
#fileName = CMVOLT_22052020.CSV
daily_volatility_file_name ="CMVOLOT_"+currentDate+currentMonthNumber+currentYear+".CSV"
daily_vol_dest_file = os.path.join(cash_report_directory,daily_volatility_file_name)
daily_vol_url ="https://www1.nseindia.com/archives/nsccl/volt/" + daily_volatility_file_name
download_csv_file(old_nse_webSession,daily_vol_url,daily_vol_dest_file)

#4. Download Bulk Deal
#####################################################################
bulk_deal_file_name = "bulk.csv"
bulk_deal_dest_file = os.path.join(cash_report_directory,bulk_deal_file_name)
bulk_deal_url ="https://www1.nseindia.com/content/equities/" + bulk_deal_file_name
download_csv_file(old_nse_webSession,bulk_deal_url,bulk_deal_dest_file)

#5. Download Block Deal
#####################################################################
block_deal_file_name = "block.csv"
block_deal_dest_file = os.path.join(cash_report_directory,block_deal_file_name)
block_deal_url ="https://www1.nseindia.com/content/equities/" + block_deal_file_name
download_csv_file(old_nse_webSession,block_deal_url,block_deal_dest_file)

#6. Download Short Selling
#####################################################################
short_sell_file_name = "ShortSelling.csv"
short_sell_dest_file = os.path.join(cash_report_directory,short_sell_file_name)
short_sell_deal_url ="https://www1.nseindia.com/content/equities/" + short_sell_file_name
download_csv_file(old_nse_webSession,short_sell_deal_url,short_sell_dest_file)

#7. Daily Delivery Report
#########################################################################
daily_del_report_file_name = "MTO_" + currentDate+currentMonthNumber+currentYear+".DAT"
daily_del_report_dest_file_name = "MTO_" + currentDate+currentMonthNumber+currentYear+".csv"
daily_del_report_url = 'https://www1.nseindia.com/archives/equities/mto/' + daily_del_report_file_name
response = old_nse_webSession.request('GET',url=daily_del_report_url).text
data = response.splitlines()[4:]
dest_file = open(os.path.join(cash_report_directory,daily_del_report_dest_file_name),"w")
dest_file.write("Sr.No,Symbol,Segment,Quantity Traded,Deliverable Quantity,% of Deliverable Quantity" + "\n")
for row_num in data:
	#print(row_num)
	dest_file.write(",".join(row_num.split(",")[1:]) + "\n")

#8. Category wise turnover
cat_wise_turn_over_file_name= "cat_turnover_"+currentDate+currentMonthNumber+currentYearShort+".xls"
cat_wise_turn_over_dest_file_name= os.path.join(CASH_ROOT_PATH,"cat_turnover_"+currentDate+currentMonthNumber+currentYearShort+".csv")
cat_wise_turn_over_url = "https://www1.nseindia.com/archives/equities/cat/" + cat_wise_turn_over_file_name
try:
	cat_wise_turn_over_data = old_nse_webSession.request('GET',cat_wise_turn_over_url).content
	cat_wise_turn_over = pd.read_excel(cat_wise_turn_over_data, skiprows=2)
	cat_wise_turn_over.drop(3, inplace=True)
	cat_wise_turn_over.to_csv(cat_wise_turn_over_dest_file_name, index=False)
except Exception as ex:
	logging.error("No Categorywise Turn over file uploaded today....")

########################################## FNO ####################################################

#1. Download Bhav Copy
#fobhavCopyFileName = "fo22MAY2020bhav.csv.zip"
fnobhavCopyFileName = "fo" + currentDate + currentMonth + currentYear+"bhav.csv.zip"
fnobhavCopyUrl = "https://www1.nseindia.com/content/historical/DERIVATIVES/" + currentYear + "/" + currentMonth +"/" + fnobhavCopyFileName

logging.debug("Downloading :" + fnobhavCopyUrl)

download_zip_file(old_nse_webSession,fnobhavCopyUrl,fno_report_directory)

#2.Open Interest
#sample : nseoi_22052020.zip
fno_oi_file_name = "nseoi_"+currentDate+currentMonthNumber+currentYear+".zip"
fno_oi_url = "https://www1.nseindia.com/archives/nsccl/mwpl/"+fno_oi_file_name
logging.debug("Downloading :" + fno_oi_url)
download_zip_file(old_nse_webSession,fno_oi_url,fno_report_directory)

#3.FII Activity in FNO
#sample:fii_stats_22-May-2020.xls
fii_stats_file_name="fii_stats_"+currentDate+"-"+currentMonthLower+"-"+currentYear+".xls"
fii_stats_dest_file_name ="fii_stats_"+currentDate+"-"+currentMonthLower+"-"+currentYear+".csv"
fii_stat_dest_path = os.path.join(fno_report_directory,fii_stats_dest_file_name)
fii_stats_url = "https://www1.nseindia.com/content/fo/"+fii_stats_file_name
fii_stats_data_xls = old_nse_webSession.request('GET',fii_stats_url).content
fii_stats_data = pd.read_excel(fii_stats_data_xls,skiprows=3)
filter_fii_stats = data = fii_stats_data.truncate(after=2)
filter_fii_stats.to_csv("/tmp/report.csv",index=False)
from_csv = pd.read_csv("/tmp/report.csv",names=["FNO Type","BUY(No. Of Contracts)","BUY(Amt. In Cr)","SELL(No. Of Contracts)","SELL(Amt. In Cr)","OI AT EOD(No. Of Contracts)","OI AT EOD(Amt. In Cr)"])
logging.debug("File Path:" + fii_stat_dest_path)
from_csv.to_csv(fii_stat_dest_path,index=False)




