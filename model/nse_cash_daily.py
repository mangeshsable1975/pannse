from sqlalchemy import Column, String
from sqlalchemy.types import *
from config.postgres_connection import base

class NseCashDaily(base):
    __tablename__ = 'nse_cash_daily'

    trade_date = Column(Date, primary_key=True)
    stock_id = Column(Integer, primary_key=True)
    stock_code = Column(String)
    series = Column(String)
    prev_close = Column(Float)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    vwap = Column(Float)
    trades = Column(Float)
    deliverable_volume = Column(Integer)
    percentage_delivery = Column(Float)
