from requests import Session
import requests
import io
import pandas as pd
pd.set_option("display.max_columns",None)
pd.set_option("display.max_rows",None)

headers = {'Accept': '*/*',
		   'Accept-Encoding': 'gzip, deflate, sdch, br',
		   'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
		   'Connection': 'keep-alive',
		   'Host': 'www1.nseindia.com',
		   'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
		   'X-Requested-With': 'XMLHttpRequest'}

webSession = requests.Session()
webSession.headers.update(headers)
# request = webSession.request('GET','https://www1.nseindia.com/archives/equities/mkt/MA200520.csv')
# url_content = request.content
# csv_file = open('downloaded.csv', 'wb')
#
# csv_file.write(url_content)
# csv_file.close()

import zipfile, urllib.request, shutil

cat_wise_turn_over_file_name= "cat_turnover_26052020.xls"
#cat_wise_turn_over_dest_file_name= os.path.join(CASH_ROOT_PATH,"cat_turnover_"+currentDate+currentMonthNumber+currentYearShort+".csv")
cat_wise_turn_over_url = "https://www1.nseindia.com/archives/equities/cat/" + cat_wise_turn_over_file_name
print(cat_wise_turn_over_url)
cat_wise_turn_over_data = webSession.request('GET',cat_wise_turn_over_url).content
print(cat_wise_turn_over_data)
#cat_wise_turn_over = pd.read_excel(cat_wise_turn_over_data,skiprows=2)
#cat_wise_turn_over.drop(3,inplace=True)
#cat_wise_turn_over.to_csv(cat_wise_turn_over_dest_file_name,index=False)
#from_csv.rename(columns={0:"FNO Type",1:"BUY(No. Of Contracts)",2:"BUY(Amt. In Cr)",3:"SELL(No. Of Contracts)",4:"SELL(Amt. In Cr)",5:"OI AT EOD(No. Of Contracts)",6:"OI AT EOD(Amt. In Cr)"},inplace=True)
#print(from_csv)
#data.to_csv("report.csv",index=False)

#print(data)
#cat_wise_turn_over.to_csv("report.csv",index=False)
#cat_wise_turn_over.drop([0,1],inplace=True)
#temp_file = open("reportfile.csv","w")
#temp_file.write("Trade Date,Category,Buy Value,Sell Value")
#for ind in cat_wise_turn_over.index:

#print(cat_wise_turn_over)


#fii_data = pd.read_(response)
#print(fii_data)