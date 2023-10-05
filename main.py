
import os
import numpy as np
import pandas as pd
import gurobipy as gp
from gurobipy import GRB

from scipy.optimize import Bounds, LinearConstraint, minimize



# Função Cria o Retorno e Log Retorno
def createTableReturns(stocksDir, save=False):
    newData = {}

    for i in stocksDir:
        stockData = pd.read_excel(f'./stocks_data/{i}')
        stockData["Normal Returns"] = stockData["Adj Close"].pct_change()
        stockData["Log Return"] = np.log(stockData["Adj Close"]/stockData["Adj Close"].shift())

        stockName = i.replace(".SA_stock_data.xlsx", "")
        newData[f'{stockName} Normal Return'] = stockData["Normal Returns"].iloc[1:]
        newData[f'{stockName} Log Return'] = stockData["Log Return"].iloc[1:]

    stockReturns = pd.DataFrame(newData)
    stockReturns = pd.concat([stockData["Date"].iloc[1:], stockReturns], axis=1)

    if save:
        stockReturns.to_excel('Stock Returns.xlsx', index=False)

    return stockReturns

# Cria o Retorno e Log Retorno
stocksDir = os.listdir('./stocks_data')

stockReturnsAll = createTableReturns(stocksDir, True)

stockReturns = stockReturnsAll.filter(like='Normal Return')
stockLogReturns = stockReturnsAll.filter(like='Log Return')

# print(stockReturnsAll)
# print(stockReturns)
# print(stockLogReturns)



# Função Cria Matriz de Variância
def covarianceMatrix(returns):
    # filteredColumns = returns.filter(like='Log')
    # print(np.var(returns, ddof=0))
    matrix = np.cov(returns, rowvar=False, bias=True)
    # matrix = filteredColumns.cov()

    return matrix

# Cria Matriz de Variância
# sla = [ # AZUL           BBAS             MRVE            PETR            UGPA           WEGE
#     [1.49235372e-03, 1.21684417e-04, 5.50237577e-04, 1.33522251e-04, 1.45952203e-04, 8.72421825e-05], # AZUL
#     [1.21684417e-04, 2.03919807e-04, 1.33856854e-04, 1.11118076e-04, 8.31303193e-05, 4.88447907e-06], # BBAS
#     [5.50237577e-04, 1.33856854e-04, 1.20386498e-03, 9.68120605e-05, 1.43025806e-04, 6.79287208e-05], # MRVE
#     [1.33522251e-04, 1.11118076e-04, 9.68120605e-05, 3.94795417e-04, 9.13359354e-05, 2.96480919e-06], # PETR
#     [1.45952203e-04, 8.31303193e-05, 1.43025806e-04, 9.13359354e-05, 3.09691135e-04, 1.18194132e-08], # UGPA
#     [8.72421825e-05, 4.88447907e-06, 6.79287208e-05, 2.96480919e-06, 1.18194132e-08, 2.13534926e-04]  # WEGE
# ]
covarMatrix = covarianceMatrix(stockLogReturns)
print(covarMatrix)



def meanStandardDeviation(returns):
    means = returns.mean()
    std = returns.std()

    return means, std

means, std = meanStandardDeviation(stockLogReturns)
print(means)
# print(std)



def createWeights(n):
    return np.ones(n)/n

weights = createWeights(6)



def riscoMarkowitz(covarMatrix, w):
    portfolioVariance = np.dot(np.dot(w, covarMatrix), w.T)

    return portfolioVariance

# weights = np.array([0, 0, 0.945, 0.055, 0, 0]) # AZUL, BBAS, MRVE, PETR, UGPA, WEGE
portfolioVariance = riscoMarkowitz(covarMatrix, weights)
# print(portfolioVariance)



def retornoMarkowitz(meanReturns, w):
    return (meanReturns * w).sum()

returnMarkowitz = retornoMarkowitz(means, weights)
# print(returnMarkowitz)



def solverMarkowtiz(logReturns, covar):
    bounds = Bounds(0, 1)

    linearConstraint = LinearConstraint(np.ones((logReturns.shape[1], ), dtype=int), 1, 1)

    pesos = np.ones(logReturns.shape[1])
    x0 = pesos/np.sum(pesos)

    fun1 = lambda w: np.sqrt(np.dot(w, np.dot(w, covar)))
    res = minimize(fun1, x0, method='trust-constr', constraints=linearConstraint, bounds=bounds)

    wOptimal = res.x

    np.set_printoptions(suppress=True, precision=2)

    return wOptimal

wOptimal = solverMarkowtiz(stockLogReturns, covarMatrix)
print(wOptimal)

def ret(r, w):
    return r.dot(w)

def vol(w,covar):
    return np.sqrt(np.dot(w,np.dot(w,covar)))

print('return: % .2f'% (ret(means, wOptimal)*100), 'risk: % .3f'% vol(wOptimal, covarMatrix))




    # model = gp.Model()

    # nAssets = len(means)
    # weight = model.addVars(nAssets, lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS, name='weight')

    # model.setObjective(sum(means[i] * weight[i] for i in range(nAssets)), GRB.MAXIMIZE)
    # model.addConstr(sum(weight[i] for i in range(nAssets)) == 1, 'sumWeights')

    # for i in range(nAssets):
    #     model.addConstr(means[i] * weight[i] <= 1, f'mean_return_{i}')

    # model.optimize()

    # return [var.x for var in weight.values()]

# print(solverMarkowtiz())

