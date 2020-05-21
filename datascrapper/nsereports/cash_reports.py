from requests import Session
import requests
import io

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

url = 'https://www1.nseindia.com/archives/equities/bhavcopy/pr/PR200520.zip'

r = webSession.request('GET',url, stream =True)
check = zipfile.is_zipfile(io.BytesIO(r.content))
while not check:
    r = requests.get(url, stream =True)
    check = zipfile.is_zipfile(io.BytesIO(r.content))
else:
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()