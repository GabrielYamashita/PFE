
# import numpy as np
# import pandas as pd
# from skimage.measure import label, regionprops

# df = pd.read_excel('./Dados/Portfolio Global - KING.xlsx', sheet_name='Política de Investimento', header=None)

# def getTables(df):
#     larr = label(np.array(df.notnull()).astype("int"))

#     list_dfs = []

#     for s in regionprops(larr):
#         sub_df = df.iloc[
#             s.bbox[0]:s.bbox[2], s.bbox[1]:s.bbox[3]
#         ].pipe(
#             lambda df_: df_.rename(columns=df_.iloc[0]).drop(df_.index[0])
#         )

#         list_dfs.append(sub_df)
#     return list_dfs

# list_dfs = getTables(df)

# for i in range(len(list_dfs)):
#     varName = f'df{i+1}'
#     value = list_dfs[i]
#     globals()[varName] = value

# print(df1.head())

def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]

# a = 10
# print(namestr(a, globals())[0])


def getValue(df):
    return namestr(df, globals())[0]

a = 1
b = 2
c = 3
d = 10
print(getValue(c))