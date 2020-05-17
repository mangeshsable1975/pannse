from sqlalchemy import Column, String
from sqlalchemy.types import *
from config.postgres_connection import base

class NseFNODaily(base):
    __tablename__ = 'nse_fno_daily'

    trade_date = Column(Date, primary_key=True)
    stock_id = Column(Integer, primary_key=True)
    stock_code = Column(String)
    expiry_date = Column(String,primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    last_price = Column(Float)
    settle_price = Column(Float)
    no_of_contracts = Column(Integer)
    open_interest = Column(Integer)
    change_in_oi = Column(Float)
    underlying = Column(Float)
