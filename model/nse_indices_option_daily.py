from sqlalchemy import Column, String
from sqlalchemy.types import *
from config.postgres_connection import base


class NseIndicesOptionDaily(base):
	__tablename__ = 'nse_indices_option_daily'
	stock_id = Column(Integer,primary_key=True)
	trade_date = Column(Date)
	stock_code = Column(String)
	strike_price = Column(Float,primary_key=True)
	option_type = Column(String,primary_key=True)
	expiry_date	= Column(Date,primary_key=True)
	identifier = Column(String)
	open_interest = Column(Integer)
	change_in_oi = Column(Integer)
	percent_change_in_oi = Column(Float)
	total_traded_volume = Column(Integer)
	implied_volatility = Column(Float)
	last_price = Column(Float)
	change = Column(Float)
	total_buy_quantity = Column(Integer)
	total_sell_quantity = Column(Integer)
	underlying_value = Column(Float)



