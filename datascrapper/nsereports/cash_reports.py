from requests import Session
import requests
import io
import pandas as pd
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

url = 'https://www1.nseindia.com/archives/equities/mto/MTO_22052020.DAT'
response = webSession.request('GET',url=url).text
data = response.splitlines()[4:]
#print(data)
dest_file = open("deliveryFile.csv","w")
dest_file.write("Sr.No,Symbol,Segment,Quantity Traded,Deliverable Quantity,% of Deliverable Quantity" + "\n")
for row_num in data:
	#print(row_num)
	dest_file.write(",".join(row_num.split(",")[1:]) + "\n")

#fii_data = pd.read_(response)
#print(fii_data)