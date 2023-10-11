



import pandas as pd

repique = pd.read_csv('C:/Users/acer/Downloads/Fintalk_1000_2709repique1110.csv', delimiter=';')
# print(repique)

formalizados = pd.read_excel('C:/Users/acer/Downloads/data (6).xlsx')
# print(formalizados)

matching_cpfs = formalizados['cpf'].tolist()
# print(len(matching_cpfs))

print(~repique['CPF_COMPLETO'].isin(matching_cpfs))
# repique.to_csv('meu_arquivo.csv', sep=';', index=False)


# merged_df = pd.merge(repique, formalizados, how='inner', left_on='CPF_COMPLETO', right_on='cpf')
# print(merged_df)

# matched_rows_from_df1 = repique[repique['CPF_COMPLETO'].isin(merged_df['CPF_COMPLETO'])]
# # print(matched_rows_from_df1)


