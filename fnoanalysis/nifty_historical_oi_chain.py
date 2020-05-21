import pandas as pd
pd.set_option("display.max_columns",None)
pd.set_option("display.max_rows",None)
import requests
attribute = {"id":"TabSymbolData"}
nifty_oi_chain = pd.read_html("https://fnoanalysis.com/oi/option_chain_hist.php?symbol=NIFTY&cmb_cnd_symbol=NIFTY&CMB_EXPIRY_DT=2020-05-28&CMB_CND_DT=2020-05-20",attrs=attribute)

column_names = ["CE OI", "Change in CE OI", "% Change in CE OI","CE Volume","CE Closing","% Chng CE Close","Strike","% Chng PE Close","PE Closing","PE Volume","% Change in PE OI","Change in PE OI","CE OI"]
option_data = pd.DataFrame(columns=column_names)

for row in nifty_oi_chain:
	for ind in range(3,111):
		for td in range(0,13):
			ce_pe_data = row[ind][td]
			print(ce_pe_data)

