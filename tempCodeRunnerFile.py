df_dados_alunos.to_sql("dados_aluno", con = connection, if_exists= "replace", index=False)
