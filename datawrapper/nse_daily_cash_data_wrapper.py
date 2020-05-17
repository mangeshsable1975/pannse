from nsepy import get_history


def get_history_wrapper(symbol, start, end, index=False, futures=False, option_type="", expiry_date=None,
                        strike_price="", series='EQ'):
    return get_history(symbol=symbol, start=start, end=end, index=index, futures=futures, option_type=option_type,
                       expiry_date=expiry_date, strike_price=strike_price, series=series)
