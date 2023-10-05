
# Imports
import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta


# Setup
if not os.path.exists('./Benchmarks'):
    os.makedirs('./Benchmarks')

excelName = 'BenchmarksData'
data = pd.DataFrame()   
data.to_excel(f'./Benchmarks/{excelName}.xlsx')

excelPath = f'./Benchmarks/{excelName}.xlsx'

benchmarks = {
    'CDI': {
        'Symbol': '^IRX'
    },
    'Ibovespa': {
        'Symbol': '^BVSP'
    },
    'S&P 500': {
        'Symbol': '^GSPC'
    },
    'IFIX': {
        'Symbol': 'IFIX.SA'
    },
    'Inflação': {
        'Symbol': '^GSPC'
    },
    # 'SMLL': {
    #     'Symbol': 'SMLL.SA'
    # }
}


# Download dos Dados
start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

for benchmark in benchmarks:
    symbol = benchmarks[benchmark]['Symbol']
    print(f'- downloading {symbol} ...')

    df = yf.download(symbol, start=start_date, end=end_date, progress=False)
    data[benchmark] = df['Adj Close']
    df.to_excel(f'./Benchmarks/{benchmark}.xlsx')

data.to_excel(excelPath)

