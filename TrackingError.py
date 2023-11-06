
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

def get_returns(ticker, period):
    start_date = (datetime.today() - timedelta(days=period)).strftime('%Y-%m-%d')
    end_date = datetime.today().strftime('%Y-%m-%d')
    data = yf.download(ticker, start=start_date, end=end_date)

    data['Return'] = data['Adj Close'].pct_change()

    return data['Return']


def calculateTrackingError(stock, benchmark='^GSPC', period=30):
    stockReturns = get_returns(stock, period)
    benchmarkReturns = get_returns(benchmark, period)

    excessReturns = stockReturns - benchmarkReturns

    trackingError = np.std(excessReturns.dropna())

    return trackingError


stock = 'AAPL'
# benchmark = '^GSPC'
period = 30

te = calculateTrackingError(stock, period=period)
print(f"The Tracking Error is {te:.2%}")
