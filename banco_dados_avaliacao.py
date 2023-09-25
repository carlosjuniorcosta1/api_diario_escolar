# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 21:55:27 2023

@author: Usuario
"""

import pandas as pd

df= pd.read_csv('bd_inserir_alunos.csv')

df_ava = df[['id']]
df_ava['nota_1'], df_ava['nota_2'], df_ava['nota_3'],\
 df_ava['nota_4'], df_ava['nota_5'], df_ava['total'] = 0, 0, 0, 0, 0, 0
 
df_ava.columns = ['avaliacao_id', 'nota_1', 
                  'nota_2', 'nota_3', 'nota_4', 'nota_5', 'total']

df_ava.to_csv('bd_avaliacao_1.csv')