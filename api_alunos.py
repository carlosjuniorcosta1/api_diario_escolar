from flask import Flask, jsonify, request
import pyodbc
import pandas as pd
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request 
from pydantic import BaseModel




app = Flask(__name__)
spec = FlaskPydanticSpec('flask', title = "Endpoints do banco de dados de alunos")
spec.register(app)

class Student(BaseModel):
    name: str
    surname: str
    full_name: str 
    grade: str
    level: str 
    age: int
    cpf: str
    id: int 
    


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



print(show_table_names)



@app.route('/diario', methods = ['GET'])
#@spec.validate(resp=Response(HTTP_200=Student))
def list_all_students():
    """Lista todos os estudantes da escola """
    db = cursor.execute(f"SELECT * FROM dados_alunos ORDER BY id DESC")
    query_st = db.fetchall()
    all_st = []
    for x in query_st:
        all_st.append({
            "nome": x[0],
            "sobrenome": x[1],
            "nome_completo": x[2],
            "ano": x[3],
            "nivel_ensino": x[4],
            "idade": x[5], 
            "cpf": x[6],
            "id" : x[7],

        })
        print(all_st)
    return jsonify(message = "Lista de todos os alunos", lista_total = all_st)
        
@app.route('/diario/', methods = ['GET'])
def list_year_level():
    """Lista por filtros """
    filter_y = request.values.get('ano')
    filter_y2 = request.values.getlist('ano')
    filter_level = request.values.getlist('nivel')    
    filter_full_name = request.values.get('nome_c')
    filter_surname = request.values.get('sobrenome')
    filter_name = request.values.get('nome')
    filter_cpf = request.values.get('cpf')
    filter_age = request.values.get('idade')
    
   
    if filter_y2 is not None:
        if len(filter_y2) == 1:        
            query_l = cursor.execute(f"SELECT * FROM dados_alunos WHERE ano = '{filter_y}'")
        
    if filter_y2 is not None:
        if len(filter_y2) >= 2:     
            
            if 'sexto' and 'setimo' in filter_y2:
                #ok
                query_l = cursor.execute(f"SELECT * FROM dados_alunos WHERE ano = 'sexto' or ano = 'setimo'")
            if 'sexto' and 'oitavo' in filter_y2:
                query_l = cursor.execute(f"SELECT * FROM dados_alunos WHERE ano = 'sexto' or ano = 'oitavo'")
            if 'sexto' and 'nono' in filter_y2:
                query_l = cursor.execute(f"""SELECT * FROM dados_alunos WHERE 
                                        ano = 'sexto' or ano = 'nono'""")           
            if 'sexto' and 'setimo' and 'oitavo' in filter_y2:
                query_l = cursor.execute(f"""SELECT * FROM dados_alunos WHERE ano = 
                                        'sexto' or ano = 'setimo' OR ano = 'oitavo'""")
            if 'sexto' and 'setimo' and 'nono' in filter_y2:
                query_l = cursor.execute(f"""SELECT * FROM dados_alunos WHERE ano = 
                                        'sexto' or ano = 'setimo' OR ano = 'nono'""")
        
    
            if 'setimo' and 'oitavo' in filter_y2:
                query_l = cursor.execute(f"""SELECT * FROM dados_alunos WHERE ano = 
                                        'setimo' OR ano = 'oitavo'""")
                
            if 'setimo' and 'oitavo' and 'nono' in filter_y2:
                query_l = cursor.execute(f"""
                                        SELECT * FROM dados_alunos WHERE ano =
                                        'setimo' OR ano = 'oitavo' OR ano = 'nono'                                     
                                        """)
            if 'oitavo' and 'nono' in filter_y2:
                query_l = cursor.execute(f"""
                                        SELECT * FROM dados_alunos WHERE ano = 
                                        'oitavo' OR ano = 'nono'                                     
                                        """)
    if filter_level is not None:
        if len(filter_level) > 0:
        
            if 'em' and 'ef' in filter_level:
                query_l= cursor.execute(f""" SELECT * FROM dados_alunos WHERE nivel_ensino = 'ef' OR 
                                        nivel_ensino = 'em'
                                        """)
            if 'ef' not in filter_level:
                query_l =  cursor.execute(f"""
                                        SELECT * FROM dados_alunos WHERE nivel_ensino = 'em'                                  
                                        """)
            if 'em' not in filter_level:
                query_l= cursor.execute(f""" SELECT * FROM dados_alunos WHERE nivel_ensino = 'ef'
                                        """)
    if filter_full_name is not None:
        if len(filter_full_name) > 0:
            query_l = cursor.execute(f"""
                                SELECT * FROM dados_alunos WHERE nome_completo
                                LIKE ?""", filter_full_name + '%')
    if filter_surname is not None:
        if len(filter_surname) > 0:
            query_l = cursor.execute(f"""
                                SELECT * FROM dados_alunos WHERE sobrenome
                                LIKE ?""", filter_surname + '%')
            
    if filter_name is not None:
        if len(filter_name) > 0:
            query_l = cursor.execute(f"""
                            SELECT * FROM dados_alunos WHERE nome
                            LIKE ?""", filter_name + '%')
    if filter_cpf is not None:
        if len(filter_cpf) > 0:
            query_l = cursor.execute(f"""
                        SELECT * FROM dados_alunos WHERE cpf
                        LIKE ?""", filter_cpf + '%')
    if filter_age is not None:
        if len(filter_age) > 0:
            query_l = cursor.execute(f"""
                                     SELECT * FROM dados_alunos WHERE idade
                                     = {filter_age}""")

    query_l = query_l.fetchall()
    list_y = []
    
    for x in query_l:
        list_y.append({
            
    "nome": x[0],
    "sobrenome": x[1],
    "nome_completo": x[2],
    "ano": x[3],
    "nivel_ensino": x[4],
    "idade": x[5], 
    "cpf": x[6], 
    "id" : x[7],

})          
        
    return jsonify(message = "Alunos por ano cursado", data = list_y)                   
           
@app.route('/diario', methods = ['POST'])

def insert_student():
    """Insere um novo estudante"""
    new_std = request.get_json(force=True)
    new_na = new_std['nome']
    new_su = new_std['sobrenome']
    new_fn = new_std['nome'] + ' ' + new_std['sobrenome']
    new_gr = new_std['ano']
    new_l = new_std['nivel_ensino']
    new_ag = new_std['idade']
    new_c = new_std['cpf']   
    cursor.execute(f""" INSERT INTO dados_alunos (nome, sobrenome, nome_completo,
                   ano, nivel_ensino, idade, cpf)
                   VALUES ('{new_na}', '{new_su}', '{new_fn}', 
                   '{new_gr}', '{new_l}', '{new_ag}', '{new_c}')
                   """)
    cursor.commit()
    return jsonify(message = "Aluno cadastrado com sucesso")
    
@app.route('/diario/deletar/<id_student>', methods = ['DELETE'])
def delete_student(id_student):

    """Deleta um estudante da lista"""
    cursor.execute(f"""
                   DELETE FROM dados_alunos WHERE id=?""", (id_student))
    cursor.commit()
    return jsonify(message = "Aluno deletado da lista. ")    
    
    
            
app.run(debug=True)