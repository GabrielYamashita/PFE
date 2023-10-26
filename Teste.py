
import pandas as pd


df1 = pd.read_csv('../../../Downloads/Fintalk_1000_2809repique1610.csv', delimiter=';')
df2 = pd.read_excel('../../../Downloads/data (6).xlsx')

print(df1)
print(df2)

# Get a list of matching CPFs
matching_cpfs = df2['cpf'].tolist()

# Remove rows in df1 that have matching CPFs
df1 = df1[~df1['CPF_COMPLETO'].isin(matching_cpfs)]

# Display the modified df1
print(df1)


# Salvar o DataFrame em um arquivo CSV com delimitador ';'
# df1.to_csv('newFintalk_1000_2809repique1610.csv', sep=';', index=False)
