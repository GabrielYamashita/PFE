
# 1. INPUTS DO EXCEL:

# todos os assets
assets = []

# pesos dos asset
weights = []

# tolerâncias dos assets
thrshs = []

# alvo dos pesos dos assets
targets = []



# 2. Buscar os Dados de Cada Assets na API
# . Pegar Quantidade de Papeis que Possuo
# . Calcular ROI (Return On Investment)
# . Checar se é Preciso Rebalancear cada Ativo (threshold)
# . Pegar o Valor Total do Portfolio
# . Calcular o Peso Alvo
# . Calcular o Valor Atual do Asset
# . Calcular o Valor Alvo do Asset
# . Calcular Quantidade de Papéis para Vender e Comprar



import yfinance as yf
from datetime import datetime, timedelta


# Informações do Excel
stocks = ['AAPL', 'GOOGL', 'NVDA', 'TSLA']
weights = [15, 25, 20, 40]
portfolioValue = 100_000
thrshs = [(5, 5), (10, 10), (2.5, 2.5), (5, 5)]
targets = [30, 15, 25, 30]


# Extraindo Dados da Yahoo Finance
# start_date = (datetime.today() - timedelta(days=1260)).strftime('%Y-%m-%d')
# end_date = datetime.today().strftime('%Y-%m-%d')
# df = yf.download(stocks, start=start_date, end=end_date)['Adj Close']


# Variáveis
myPortfolio = {}


# Funções Importantes

## 
def getExcelData():
    pass


## 
def buildPortfolioData(portfolio, stocks, weights, targets, thresholds):
    for i in range(len(stocks)):
        portfolio[stocks[i]] = dict(CurrentWeight=weights[i], Target=targets[i], Thresholds=thresholds[i])
    
    # print(portfolio)

buildPortfolioData(myPortfolio, stocks, weights, targets, thrshs)


## 
def getCurrentPrices(portfolio, tickers):
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        currPrice = stock.history(period='1d')['Close'].iloc[0]
        portfolio[ticker]["CurrentStockPrice"] = currPrice
    
    # print(portfolio)

getCurrentPrices(myPortfolio, stocks)


## 
def getCurrentPortfolioValue(portfolio, pValue):
    for stock in portfolio:
        myPortfolio[stock]["PortfolioStockValue"] = pValue * myPortfolio[stock]["CurrentWeight"]/100

    # print(portfolio)

getCurrentPortfolioValue(myPortfolio, portfolioValue)


##
def checkRebalance(portfolio):
    for stock in portfolio:
        thrshUP, thrshDOWN = myPortfolio[stock]["Thresholds"]
        currWeight = myPortfolio[stock]["CurrentWeight"]
        target = myPortfolio[stock]["Target"]

        if target-thrshDOWN < currWeight < target+thrshUP:
            portfolio[stock]['NeedRebalance'] = False

        else:
            portfolio[stock]['NeedRebalance'] = True

    # print(portfolio)

checkRebalance(myPortfolio)


##
def rebalancePortfolio(portfolio, pValue):
    if any([i["NeedRebalance"] for i in portfolio.values()]):
        for stock in portfolio:
            currWeight = portfolio[stock]["CurrentWeight"]
            target = portfolio[stock]["Target"]

            offset = currWeight-target
            portfolio[stock]["Offset"] = offset

            if offset < 0:
                order = 'Buy'

            elif offset > 0:
                order = 'Sell'

            portfolio[stock]["Order"] = order
        
        sumSell = 0
        for stock in portfolio:
            if portfolio[stock]["Order"] == 'Sell':
                portfolioStockValue = portfolio[stock]["PortfolioStockValue"]
                currStockPrice = portfolio[stock]["CurrentStockPrice"]

                offset = portfolio[stock]["Offset"]
                sellValue = offset/100 * pValue

                sellPapers = sellValue//currStockPrice
                portfolio[stock]["QuantityPapers"] = sellPapers

                sellValue = currStockPrice * sellPapers
                sumSell += sellValue
                portfolio[stock]["RebalancePortfolioValue"] = portfolioStockValue - sellValue

        for stock in portfolio:
            if portfolio[stock]["Order"] == 'Buy':
                portfolioStockValue = portfolio[stock]["PortfolioStockValue"]
                currStockPrice = portfolio[stock]["CurrentStockPrice"]

                offset = portfolio[stock]["Offset"]
                buyValue = offset/100 * sumSell
                buyValue = sumSell

                buyPapers = buyValue//currStockPrice
                portfolio[stock]["QuantityPapers"] = buyPapers

                buyValue = currStockPrice * buyPapers
                sumSell -= buyValue
                portfolio[stock]["RebalancePortfolioValue"] = portfolioStockValue + buyValue

        print(portfolio)
        return sumSell

surplus = rebalancePortfolio(myPortfolio, portfolioValue)


##
def returnOrders(portfolio, surplus):
    new_pValue = sum([i["RebalancePortfolioValue"] for i in portfolio.values()])

    print(f"New Portfolio Value: {new_pValue}")
    print(f"Surplus Capital: {surplus}\n")
    
    for stock in portfolio:
        order = portfolio[stock]["Order"]
        qntPapers = abs(portfolio[stock]["QuantityPapers"])
        rebalancePValue = portfolio[stock]["RebalancePortfolioValue"]
        newWeight = rebalancePValue/new_pValue

        print(f"[{stock}]\n- {order} {qntPapers} papers\n- New Weight {newWeight:.2%}\n\n")
    

returnOrders(myPortfolio, surplus)