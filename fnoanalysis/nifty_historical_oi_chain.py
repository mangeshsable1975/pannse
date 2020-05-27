import pandas as pd
import requests
from datetime import datetime
from datascrapper import nse_utils
from utils import nse_supportive_functions

pd.set_option("display.max_columns",None)
pd.set_option("display.max_rows",None)


from_date = datetime(2020,5,1)
to_date = datetime.today()

holiday_list = nse_supportive_functions.get_nse_holiday_list()
print(holiday_list)

working_days = nse_supportive_functions.get_working_days(from_date,to_date)
print(working_days)
# attribute = {"id":"TabSymbolData"}
# nifty_oi_chain = pd.read_html("https://fnoanalysis.com/oi/option_chain_hist.php?symbol=NIFTY&cmb_cnd_symbol=NIFTY&CMB_EXPIRY_DT=2020-05-28&CMB_CND_DT=2020-05-20",attrs=attribute)
#
# column_names = ["CE OI", "Change in CE OI", "% Change in CE OI","CE Volume","CE Closing","% Chng CE Close","Strike","% Chng PE Close","PE Closing","PE Volume","% Change in PE OI","Change in PE OI","CE OI"]
# option_data = pd.DataFrame(columns=column_names)
# nifty_oi_chain_data = nifty_oi_chain[0]
# nifty_oi_chain_data.drop([0,1,2],inplace=True)
# nifty_oi_filter_data = nifty_oi_chain_data.replace('-',0.0)
# data = nifty_oi_filter_data.rename(columns={0:"CE OI",1:"Change in CE OI",2:"% Change in CE OI",3:"CE Volume",4:"CE Closing",5:"% Chng CE Close",6:"Strike",7:"% Chng PE Close",8:"PE Closing",9:"PE Volume",10:"% Change in PE OI",11:"Change in PE OI",12:"PE OI"})
# data.reset_index(drop=True,inplace=True)
# json_data = data.to_json(orient='records')
# print(json_data)
#print(data)
#print(type(data.index))
# for i in range(len(data)):
# 	print(data.iloc[i,"CE OI"])
#duplicated = data.index.duplicated(keep=False)
#print(duplicated)
# for ind in data.index:
# 	#print(ind)
# 	print(data["CE OI"][ind])
# 	print("####################")


