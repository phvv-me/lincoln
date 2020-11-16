import yfinance
from pandas_datareader import data as pdr

yfinance.pdr_override()


def fetch_from_yahoo(all_symbols):
    symbols_str = " ".join(all_symbols)
    data = pdr.get_data_yahoo(symbols_str, period="5d", interval="30m").fillna(method='ffill').fillna(method='bfill')
    return data.swaplevel(axis=1) if len(all_symbols) > 1 else data
