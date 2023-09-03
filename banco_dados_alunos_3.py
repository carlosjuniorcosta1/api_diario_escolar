# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 18:54:55 2023

@author: Usuario
"""

import pandas as pd
import random
import numpy as np

df = pd.read_csv('dados_alunos.csv')

df.drop('Unnamed: 0', axis = 1, inplace=True)

df.drop("Unnamed: 0", axis = 1, inplace=True)

df_dados_alunos = df.loc[:, "nome" : "idade"]

df_dados_alunos['cpf'] = 0

df_dados_alunos['cpf']  = df_dados_alunos['cpf'].apply(lambda x: random.randrange(0, 99999999999, 2))
df_dados_alunos['cpf'] = df_dados_alunos['cpf'].astype('string')

random.seed(123)
df_dados_alunos['idade'] = df_dados_alunos['idade'].apply(lambda x: random.randrange(11, 18))

lista = []
for x in df_dados_alunos['idade'].values:
    if x == 11:
        lista.append("sexto")
    elif x == 12: 
        lista.append("setimo")
    elif x == 13:
        lista.append("oitavo")
    elif x == 14:
        lista.append("nono")
    elif x == 15:
        lista.append("primeiro_em")
    elif x == 16:
        lista.append("segundo_em")
    elif x == 17:
        lista.append("terceiro_em")
    elif x == 18:
        lista.append("terceiro_em")
print(lista)

df_dados_alunos['ano'] = lista


lista2= []
for x in df_dados_alunos['ano'].values:
    if x in ["sexto", 'setimo', 'oitavo', 'nono']:
        lista2.append("ef")
    else:
        lista2.append("em")
    
df_dados_alunos['nivel_ensino'] = lista2

df.drop('Unnamed: 0', axis = 1, inplace = True)



df.to_csv('dados_alunos.csv')

df_dados_alunos.to_csv('dados_alunos.csv')


for y in range(206):
    print(f"UPDATE dados_alunos SET turma {random.randint(1,4)}  WHERE id = {y},")
    
    
import random
random.randint(1,4)
    
