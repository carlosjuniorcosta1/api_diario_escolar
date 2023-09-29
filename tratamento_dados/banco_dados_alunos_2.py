# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 19:56:51 2023

@author: Usuario
"""

import pandas as pd 
from sqlalchemy import create_engine

engine = create_engine('sqlite://', echo=False)

df = pd.read_csv('bd_alunos.csv')

df.to_sql("teste_alunos", con = engine)

df.drop(['Unnamed: 0', 'id'], axis = 1, inplace=True)



print(engine.execute("SELECT * FROM teste_alunos").fetchall())

df.insert(2, "nome_completo", df['nome'] + ' '+ df['sobrenome'])

df.insert(6, "data_aula", "" )
 
df.drop('data_aula', axis= 1, inplace=True)

pd.to_datetime(df['data_aula'])

df.columns = ['nome', 'sobrenome', 'ano', 'nivel_ensino', 'idade', 'falta_bimestral',
       'falta_anual', 'nota_bimestral', 'nota_anual',
       'aproveitamento_bimestral', 'aproveitamento_anual', 'media_turma',
       'situacao_bimestral', 'situacao_anual']

df.to_csv("bd_alunos.csv")