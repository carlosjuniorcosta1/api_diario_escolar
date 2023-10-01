from flask import Flask, jsonify, request
import pyodbc
import pandas as pd
from flask_pydantic_spec import FlaskPydanticSpec
from pydantic import BaseModel


app = Flask(__name__)
spec = FlaskPydanticSpec('flask', title = "Endpoints da api para inserir alunos")
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
    "Database=bncc;"  
    "Trusted_connection=YES;"
)

connection = pyodbc.connect(data_for_connection)
cursor = connection.cursor()

show_table_names = cursor.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES \
                                  WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG='bd_alunos'")

show_table_names = show_table_names.fetchall()



@app.route('/diario', methods = ['GET'])
#@spec.validate(resp=Response(HTTP_200=Student))
def list_all_students():
    """Lista todos os estudantes da escola """
    db = cursor.execute(f"SELECT * FROM tabela_alunos ORDER BY id_aluno DESC")
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
            "turma": x[8]

        })
    return jsonify(message = "Lista de todos os alunos", lista_total = all_st)

@app.route('/diario/aluno/<id_student>', methods = ['GET'])
def list_student_by_id(id_student):
    "Lista os dados de um estudante pelo id"
    db = cursor.execute(f"SELECT * FROM tabela_alunos where id_aluno = ?", (id_student) )
    query_data = db.fetchall()
    query_l = []
    for x in query_data:
        query_l.append({
            "nome": x[0],
            "sobrenome": x[1],
            "nome_completo": x[2],
            "ano": x[3],
            "nivel_ensino": x[4],
            "idade": x[5], 
            "cpf": x[6],
            "turma": x[8]
            
        })
        return jsonify(data = query_l, message = "Aluno solicitado")
 
@app.route('/diario/', methods = ['GET'])
def list_filters():
    """Lista por filtros - id, ano, nivel, nome, sobrenome, nome_c, cpf, idade """
    filter_y = request.values.get('ano')
    filter_y2 = request.values.getlist('ano')
    filter_level = request.values.getlist('nivel')    
    filter_full_name = request.values.get('nome_c')
    filter_surname = request.values.get('sobrenome')
    filter_name = request.values.get('nome')
    filter_cpf = request.values.get('cpf')
    filter_age = request.values.get('idade')
    filter_id = request.values.get('id')
    
   
    if filter_y2 is not None:
        if len(filter_y2) == 1:        
            query_l = cursor.execute(f"SELECT * FROM tabela_alunos WHERE ano = '{filter_y}'")
        
    if filter_y2 is not None:
        if len(filter_y2) >= 2:     
            
            if 'sexto' and 'setimo' in filter_y2:
                #ok
                query_l = cursor.execute(f"SELECT * FROM tabela_alunos WHERE ano = 'sexto' or ano = 'setimo'")
            if 'sexto' and 'oitavo' in filter_y2:
                query_l = cursor.execute(f"SELECT * FROM tabela_alunos WHERE ano = 'sexto' or ano = 'oitavo'")
            if 'sexto' and 'nono' in filter_y2:
                query_l = cursor.execute(f"""SELECT * FROM tabela_alunos WHERE 
                                        ano = 'sexto' or ano = 'nono'""")           
            if 'sexto' and 'setimo' and 'oitavo' in filter_y2:
                query_l = cursor.execute(f"""SELECT * FROM tabela_alunos WHERE ano = 
                                        'sexto' or ano = 'setimo' OR ano = 'oitavo'""")
            if 'sexto' and 'setimo' and 'nono' in filter_y2:
                query_l = cursor.execute(f"""SELECT * FROM tabela_alunos WHERE ano = 
                                        'sexto' or ano = 'setimo' OR ano = 'nono'""")
        
    
            if 'setimo' and 'oitavo' in filter_y2:
                query_l = cursor.execute(f"""SELECT * FROM tabela_alunos WHERE ano = 
                                        'setimo' OR ano = 'oitavo'""")
                
            if 'setimo' and 'oitavo' and 'nono' in filter_y2:
                query_l = cursor.execute(f"""
                                        SELECT * FROM tabela_alunos WHERE ano =
                                        'setimo' OR ano = 'oitavo' OR ano = 'nono'                                     
                                        """)
            if 'oitavo' and 'nono' in filter_y2:
                query_l = cursor.execute(f"""
                                        SELECT * FROM tabela_alunos WHERE ano = 
                                        'oitavo' OR ano = 'nono'                                     
                                        """)
    if filter_level is not None:
        if len(filter_level) > 0:
        
            if 'em' and 'ef' in filter_level:
                query_l= cursor.execute(f""" SELECT * FROM tabela_alunos WHERE nivel_ensino = 'ef' OR 
                                        nivel_ensino = 'em'
                                        """)
            if 'ef' not in filter_level:
                query_l =  cursor.execute(f"""
                                        SELECT * FROM tabela_alunos WHERE nivel_ensino = 'em'                                  
                                        """)
            if 'em' not in filter_level:
                query_l= cursor.execute(f""" SELECT * FROM tabela_alunos WHERE nivel_ensino = 'ef'
                                        """)
    if filter_full_name is not None:
        if len(filter_full_name) > 0:
            query_l = cursor.execute(f"""
                                SELECT * FROM tabela_alunos WHERE nome_completo
                                LIKE ?""", filter_full_name + '%')
    if filter_surname is not None:
        if len(filter_surname) > 0:
            query_l = cursor.execute(f"""
                                SELECT * FROM tabela_alunos WHERE sobrenome
                                LIKE ?""", filter_surname + '%')
            
    if filter_name is not None:
        if len(filter_name) > 0:
            query_l = cursor.execute(f"""
                            SELECT * FROM tabela_alunos WHERE nome
                            LIKE ?""", filter_name + '%')
    if filter_cpf is not None:
        if len(filter_cpf) > 0:
            query_l = cursor.execute(f"""
                        SELECT * FROM tabela_alunos WHERE cpf
                        LIKE ?""", filter_cpf + '%')
    if filter_age is not None:
        if len(filter_age) > 0:
            query_l = cursor.execute(f"""
                                     SELECT * FROM tabela_alunos WHERE idade
                                     = {filter_age}""")
    if filter_id is not None:
        query_l = cursor.execute(f"""
                                 SELECT * FROM tabela_alunos WHERE id_aluno= {filter_id}""")
    

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
    "turma": x[8]

})          
        
    return jsonify(message = "Alunos por ano cursado", data = list_y)                   
           
@app.route('/diario/inserir', methods = ['POST'])

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
    new_cl = new_std['turma']
    cursor.execute(f""" INSERT INTO tabela_alunos (nome, sobrenome, nome_completo,
                   ano, nivel_ensino, idade, cpf, turma)
                   VALUES ('{new_na}', '{new_su}', '{new_fn}', 
                   '{new_gr}', '{new_l}', '{new_ag}', '{new_c}', {new_cl})
                   """)
    cursor.commit()
    return jsonify(message = "Aluno cadastrado com sucesso")
    
@app.route('/diario/deletar/<id_student>', methods = ['DELETE'])
def delete_student(id_student):

    """Deleta um estudante da lista"""
    cursor.execute(f"""
                   DELETE FROM tabela_alunos WHERE id_aluno=?""", (id_student))
    cursor.commit()
    return jsonify(message = "Aluno deletado da lista. ")    
    
    
@app.route('/diario/atualizar/<id_student>', methods = ['PUT'])
def update_std(id_student):
    """Atualiza um estudante da lista"""
  
    updated_data = request.get_json(force=True)
    up_na = updated_data['nome']
    up_su = updated_data['sobrenome']
    up_fn =updated_data['nome'] + updated_data['sobrenome']
    up_gr = updated_data['ano']
    up_le = updated_data['nivel_ensino']
    up_ag = updated_data['idade']
    up_cpf = updated_data['cpf']
    up_cl = updated_data['turma']
    
    cursor.execute(f"""UPDATE tabela_alunos SET nome = '{up_na}', 
                   sobrenome = '{up_su}', nome_completo = '{up_fn}',
                   ano = '{up_gr}', nivel_ensino = '{up_le}', 
                   idade = {up_ag}, cpf = '{up_cpf}', turma = {up_cl} WHERE id_aluno ={id_student}
                   """)
    
    cursor.commit()
    return(jsonify(message = "Estudante com get"))
    
    
app.run(debug=True)