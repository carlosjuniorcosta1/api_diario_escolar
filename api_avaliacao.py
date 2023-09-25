from flask import Flask, jsonify, request
import pyodbc
import pandas as pd
from flask_pydantic_spec import FlaskPydanticSpec




app = Flask(__name__)
spec = FlaskPydanticSpec('flask', title = "Endpoints do banco de dados de alunos")
spec.register(app)

data_for_connection = (
    "Driver={SQL Server Native Client RDA 11.0};"
    "Server=DESKTOP-1698A6Q\SQLEXPRESS;"
    "Database=bd_alunos;"  
    "Trusted_connection=YES;"
)
connection = pyodbc.connect(data_for_connection)
cursor = connection.cursor()
show_table_names = cursor.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES \
                                  WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG='bd_alunos'")
show_table_names = show_table_names.fetchall()


df = pd.read_sql(f"select * from dados_alunos", con= connection)

df_pd = pd.DataFrame(df)
print(df_pd)

df_pd.to_csv('bd_inserir_alunos.csv')