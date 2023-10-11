
# Import de Bibliotecas
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta


# Funções Importantes
def invest(df, stocks, i, amount):
    c = dict([(col, j) for j, col in enumerate(df.columns)])
    halfValue = amount/2
    # print(stocks)

    for stock in stocks:
        df.iloc[i:, c[f'sh {stock}']] = halfValue/df.iloc[i, c[f'{stock}']]
        # df.iloc[i:, c['sh AAPL']] = halfValue/df.iloc[i, c['AAPL']]

        df.iloc[i:, c[f'{stock} Value']] = (
            df.iloc[i:, c[f'{stock}']] * df.iloc[i:, c[f'sh {stock}']]
        )
        # df.iloc[i:, c['AAPL Value']] = (
        #     df.iloc[i:, c['AAPL']] * df.iloc[i:, c['sh AAPL']]
        # )

    df.iloc[i:, c['ratio']] = (
        df.iloc[i:, c[f'{stocks[0]} Value']]/df.iloc[i:, c[f'{stocks[1]} Value']]
    )


def rebalance(df, stocks, tol, i=0):
    c = dict([(col, j) for j, col in enumerate(df.columns)])
    # print(stocks)

    while True:
        mask = np.logical_or(df['ratio'] >= 1+tol, df['ratio'] <= 1-tol)

        mask[:i] = False
        try:
            i = np.where(mask)[0][0] + 1

        except IndexError:
            break
        
        # amount = (df.iloc[i, c[f'IBM Value']] + df.iloc[i, c[f'AAPL Value']])

        amount = 0
        for stock in stocks:
            amount += df.iloc[i, c[f'{stock} Value']]

        invest(df, stocks, i, amount)

    return df


# Informações do Excel
stocks = ['TSLA', 'AAPL']
bandwidth = 0.1


# Extraindo Dados da "API"
start_date = (datetime.today() - timedelta(days=1260)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

df = yf.download(stocks, start=start_date, end=end_date)['Adj Close']

for stock in stocks:
    df[f'sh {stock}'] = 0      # Excel
    df[f'{stock} Value'] = 0   # API

# df['sh AAPL'] = 0     # Excel
# df['AAPL Value'] = 0  # API
df['ratio'] = 0       # Código


# Usando as Funções
invest(df, stocks, i=0, amount=1000)
rebalance(df, stocks, bandwidth)


# Informações Importantes
df['Portfolio Value'] = df[f'{stocks[0]} Value'] + df[f'{stocks[1]} Value']

for stock in stocks:
    df[f'{stock} Weight'] = df[f'{stock} Value']/df['Portfolio Value']
# df['AAPL Weight'] = df['AAPL Value']/df['Portfolio Value']


for stock in stocks:
    print(f"{stock} Weight (min): {df[f'{stock} Weight'].min():.2%}")
    print(f"{stock} Weight (max): {df[f'{stock} Weight'].max():.2%}")

# print(f"AAPL Weight (max): {df['AAPL Weight'].min():.2%}")
# print(f"AAPL Weight (min): {df['AAPL Weight'].max():.2%}")

# # Linhas que Precisou de Rebalanceamento
# mask = np.logical_or(df['ratio'] >= 1+bandwidth, df['ratio'] <= 1-bandwidth)
# # print(mask)
# print(f"\nLinhas de Rebalanceamento:\n{df.loc[mask]}")

# print(df)


# Salvando em Excel
df.to_excel('Rebalanceamento.xlsx')
