# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 21:55:27 2023

@author: Usuario
"""

import pandas as pd
import random 

df= pd.read_csv('tabela_avaliacao.csv')

df['nota_1'] = df['nota_1'].apply(lambda x: random.randrange(0,5,1))
df['nota_2'] = df['nota_2'].apply(lambda x: random.randrange(0,5,1))
df['nota_3'] = df['nota_3'].apply(lambda x: random.randrange(0,5,1))
df['nota_4'] = df['nota_4'].apply(lambda x: random.randrange(0,5,1))
df['total'] = df['nota_1'] + df['nota_2'] + df['nota_3'] + df['nota_4']




df_ava = df[['id']]
df_ava['nota_1'], df_ava['nota_2'], df_ava['nota_3'],\
 df_ava['nota_4'], df_ava['nota_5'], df_ava['total'] = 0, 0, 0, 0, 0, 0
 
df_ava.columns = ['avaliacao_id', 'nota_1', 
                  'nota_2', 'nota_3', 'nota_4', 'nota_5', 'total']
df.drop('Unnamed: 0', axis = 1, inplace=True)

df.to_csv('tabela_avaliacao.csv')


df.columns = ['id_aluno', 'id_avaliacao', 'nota_1', 'nota_2', 'nota_3', 'nota_4',
       'nota_5', 'total']
df.drop('id_bimestre', axis =1, inplace = True)
df.insert(1, 'id_bimestre', 0)
df['id_bimestre'] = df['id_bimestre'].apply(lambda x: random.randrange(1,5,1))

df.to_csv('tabela_avaliacao')

df['id_aluno'] = df['id_aluno'].apply(lambda x:  random.randrange(0,50,1))