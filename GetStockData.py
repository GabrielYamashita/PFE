import yfinance as yf
from datetime import datetime, timedelta

# Define the ticker symbols for the stocks
tickers = ['AZUL4.SA', 'BBAS3.SA', 'MRVE3.SA', 'PETR4.SA', 'UGPA3.SA', 'WEGE3.SA']
start_date = (datetime.today() - timedelta(days=90)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

allInOne = False

if allInOne:
    # Fetch historical data
    data = yf.download(tickers, start=start_date, end=end_date)

    # Save the data to an Excel file
    data.to_excel('stock_data.xlsx')

else:
    for i in tickers:
        # Fetch historical data
        data = yf.download(i, start=start_date, end=end_date)

        # Save the data to an Excel file
        data.to_excel(f'./stocks_data/{i}_stock_data.xlsx')

