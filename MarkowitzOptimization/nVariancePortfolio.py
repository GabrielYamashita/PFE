
# --- #

import itertools

# --- #

# 1 2 3 4 5
pesosAcoes = [1, 2, 3, 4, 5, 6]
print(pesosAcoes)

# 2 3 4 5 6
variaAcoes = [2, 3, 4, 5, 6, 7]
print(variaAcoes)

# 1 2 3 4 5 6 7 8 9 10 (para 5 ações)
def calcIterations(n):
    return int( (n*n - n) / 2 )

print(calcIterations(4))

covarAcoes = list(range(1, calcIterations(len(pesosAcoes))+1))
print(covarAcoes)

# --- #

def varianciaPortfolio(pesosAcoes, variaAcoes, covarAcoes):
    firstPart = 0
    for i in range(len(pesosAcoes)):
        peso = pesosAcoes[i]**2
        variacao = variaAcoes[i]

        indivPart = peso * variacao
        print(indivPart)
        firstPart += indivPart
    # print(firstPart)


    combinations = list(itertools.combinations(pesosAcoes, 2))

    secondPart = 0
    for i in range(len(combinations)):
        indivPart = 1
        for j in range(len(combinations[i])):
            indivPart *= combinations[i][j]
        
        indivPart *= 2*covarAcoes[i]
        print(indivPart)
        secondPart += indivPart
    # print(secondPart)

    return firstPart + secondPart

# --- #

print("")

varPortfolio = varianciaPortfolio(pesosAcoes, variaAcoes, covarAcoes)
print(varPortfolio)




