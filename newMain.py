
# Importanto Bibliotecas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import Bounds, LinearConstraint, minimize


# Importanto Dados das Ações
df = pd.read_excel(r'./data/stocks.xlsx',header = 0).set_index('Date')
# print(df.head())


# Plotando as Ações
plt.figure(figsize=(15, 6))
for i in range(df.shape[1]):
    plt.plot(df.iloc[:,i], label=df.columns.values[i])

plt.legend(loc='upper left', fontsize=12)
plt.ylabel('Price in $')
# plt.show()


# Plotando as Ações Normalizadas
dfNormalized = df.divide(df.iloc[0] / 100)
# print(dfNormalized.head())

plt.figure(figsize=(15, 6))
for i in range(dfNormalized.shape[1]):
    plt.plot(dfNormalized.iloc[:,i], label=dfNormalized.columns.values[i])

plt.legend(loc='upper left', fontsize=12)
plt.ylabel('Normalized prices')
# plt.show()


# Retorno Médio
r = np.mean(df, axis=0)
# print(r)

# Matriz de Covariânica
covar = pd.DataFrame(np.cov(df, rowvar=False, bias=True))
# print(covar)


# Taxa de Retorno
def ret(r, w):
    return r.dot(w)

# Volatilidade
def vol(w, covar):
    return np.sqrt(np.dot(w, np.dot(w, covar)))

# Sharpe
def sharpe (ret,vol):
    return ret/vol


# Achando o Peso Ótimo
bounds = Bounds(0, 1) # Restrição: Limites dos Pesos [0, 1]
linear_constraint = LinearConstraint(np.ones((df.shape[1], ), dtype=int), 1, 1) # Restrição: Soma dos Pesos tem que Ser 1

# Procurando os Pesos do Portfólio com Menor Risco
weights = np.ones(df.shape[1])
x0 = weights/np.sum(weights)
fun1 = lambda w: np.sqrt(np.dot(w, np.dot(w, covar)))
res = minimize(fun1, x0, method='trust-constr', constraints=linear_constraint, bounds=bounds)
w_min = res.x

# Pesos Ótimos para o Menor Risco
np.set_printoptions(suppress=True, precision=3)
print(w_min)
print(f'return: {ret(r, w_min):.2%}\nrisk: {vol(w_min, covar):.3f}\n')


# Procurando os Pesos do Portfólio com Maior Índice de Sharpe
#Define 1/Sharpe_ratio
fun2 = lambda w: np.sqrt(np.dot(w, np.dot(w, covar)))/r.dot(w)
res_sharpe = minimize(fun2, x0, method='trust-constr', constraints=linear_constraint, bounds=bounds)

# Pesos Ótimos para o Maior Índice de Sharpe
w_sharpe = res_sharpe.x
print(w_sharpe)
print(f'return: {ret(r, w_min):.2%}\nrisk: {vol(w_min, covar):.3f}\n')


# Plotando a Fronteira Eficiente
w = w_min
num_ports = 100
gap = (np.amax(r) - ret(r, w_min))/num_ports

all_weights = np.zeros((num_ports, len(df.columns)))
all_weights[0],all_weights[1] = w_min, w_sharpe
ret_arr = np.zeros(num_ports)
ret_arr[0], ret_arr[1] = ret(r, w_min), ret(r, w_sharpe)
vol_arr = np.zeros(num_ports)
vol_arr[0], vol_arr[1] = vol(w_min, covar), vol(w_sharpe, covar)

for i in range(num_ports):
    port_ret = ret(r, w) + i*gap
    double_constraint = LinearConstraint([np.ones(df.shape[1]), r], [1, port_ret], [1, port_ret])
    
    # x0 = Palpite Inicial para os Pesos
    x0 = w_min

    # Volatilidade do Portfólio
    fun = lambda w: np.sqrt(np.dot(w, np.dot(w, covar)))
    a = minimize(fun, x0, method='trust-constr', constraints=double_constraint, bounds=bounds)
    
    all_weights[i,:] = a.x
    ret_arr[i] = port_ret
    vol_arr[i] = vol(a.x,covar)

sharpe_arr = ret_arr/vol_arr  

plt.figure(figsize=(20,10))
plt.scatter(vol_arr, ret_arr, c=sharpe_arr, cmap='viridis')
plt.colorbar(label='Sharpe Ratio')
plt.xlabel('Volatility')
plt.ylabel('Return')
plt.show()
