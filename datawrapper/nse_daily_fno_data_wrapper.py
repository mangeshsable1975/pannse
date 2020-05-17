from nsepy.derivatives import get_expiry_date


def get_expiry_date_wrapper(year, month, index=True, stock=False, vix=False, recursion=0):
    return get_expiry_date(year=year, month=month, index=index, stock=stock, vix=vix, recursion=recursion)
