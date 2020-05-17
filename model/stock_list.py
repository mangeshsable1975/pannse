from sqlalchemy import Column, String
from sqlalchemy.types import *
from config.postgres_connection import base


class StockList(base):
    __tablename__ = 'stock_list'

    stock_id = Column(Integer, primary_key=True)
    stock_code = Column(String)
    stock_description = Column(String)
    nifty50 = Column(Boolean)
    nifty100 = Column(Boolean)
    nifty500 = Column(Boolean)
    downloaded = Column(Boolean)
    fno = Column(Boolean)
    indices = Column(Boolean)
