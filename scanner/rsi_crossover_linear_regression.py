import talib
from sklearn.linear_model import LinearRegression

from config.postgres_connection import *
from datetime import datetime,timedelta
from config.postgres_connection import session
from model.nse_cash_daily import NseCashDaily
from model.stock_list import StockList
import pandas as pd
from sqlalchemy import asc,desc
import numpy as np
pd.set_option('display.max_columns', None)

from talib import *

rsiPeriod = 14
todaysDate = datetime.today()
rsiPeriodDate = todaysDate - timedelta(days=rsiPeriod)


stocks = session.query(StockList).filter(StockList.nifty50 == True).filter(StockList.stock_code =='TCS')

for stock in stocks:
    nse_cash_daily = session.query(NseCashDaily).filter(NseCashDaily.stock_code == stock.stock_code).order_by(asc(NseCashDaily.trade_date))
    print(nse_cash_daily.statement)
    stock_data_df = pd.read_sql(nse_cash_daily.statement,db)
    #print(stock_data_df.head())
    rsiValue = talib.RSI(stock_data_df["close"],timeperiod=14)
    #print("RSI (first 10 elements)\n", rsiValue[14:24])
    x = np.array(stock_data_df["close"]).reshape(-1, 1)
    rsiValue.fillna(0, inplace=True)
    y = np.array(rsiValue)
    print(x)
    print(y)

    model = LinearRegression()
    model.fit(x, y)
    r_sq = model.score(x, y)
    print('coefficient of determination:', r_sq)




