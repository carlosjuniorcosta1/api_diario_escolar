# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd

df = pd.read_excel('1.xls')
df['id'] = 0
df['ano'] = ""
df['nivel_ensino'] = ""
df['idade'] = 0
df['falta_bimestral'] = 0
df['falta_anual'] = 0
df['nota_bimestral'] = 0
df['nota_anual'] = 0
df['aproveitamento_bimestral'] = 0
df['aproveitamento_anual'] = 0
df['media_turma'] = 0.0 
df['situacao_bimestral'] = ""
df['situacao_anual'] = ""

df.columns = ['Unnamed:0','id','nome', ' sobrenome', 'ano', 'nivel_ensino', 'idade',
       'falta_bimestral', 'falta_anual', 'nota_bimestral', 'nota_anual',
       'aproveitamento_bimestral', 'aproveitamento_anual', 'media_turma',
       'situacao_bimestral', 'situacao_anual']
df.drop('Unnamed:0', axis=1, inplace=True)
df = df[['id','nome', ' sobrenome', 'ano', 'nivel_ensino', 'idade',
       'falta_bimestral', 'falta_anual', 'nota_bimestral', 'nota_anual',
       'aproveitamento_bimestral', 'aproveitamento_anual', 'media_turma',
       'situacao_bimestral', 'situacao_anual']]

df.to_csv("bd_alunos.csv")



df = pd.read_csv('bd_alunos.csv')


