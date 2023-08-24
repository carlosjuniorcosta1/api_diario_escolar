from flask import Flask, jsonify, request
import pyodbc
import pandas as pd

app = Flask(__name__)

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

for x in table_names:
    print(x)

@app.route('/diario', methods = ['GET'])
def list_all_students():
    cursor = connection.cursor()
    db = cursor.execute(f"SELECT * FROM dados_alunos")
    query_st = db.fetchall()
    all_st = []
    for x in query_st:
        all_st.append({
            "column1" : x[0],
            "nome": x[1],
            "sobrenome": x[2],
            "nome_completo": x[3],
            "ano": x[4],
            "nivel_ensino": x[5],
            "idade": x[6], 
            "cpf": x[7]
        })
        print(all_st)
    return jsonify(message = "Lista de todos os alunos", lista_total = all_st)
        
@app.route('/diario/', methods = ['GET'])
def list_all_par():
    filter_y = request.values.get('ano')
    filter_y2 = request.values.getlist('ano')
    filter_level = request.values.getlist('nivel')
    if len(filter_y2) == 1:        
        query_l = cursor.execute(f"SELECT * FROM dados_alunos WHERE ano = '{filter_y}'")
        
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
          
        

    query_l = query_l.fetchall()
    list_y = []
    
    for x in query_l:
        list_y.append({
            
    "column1" : x[0],
    "nome": x[1],
    "sobrenome": x[2],
    "nome_completo": x[3],
    "ano": x[4],
    "nivel_ensino": x[5],
    "idade": x[6], 
    "cpf": x[7]
})
            
        
    return jsonify(message = "Alunos por ano cursado", data = list_y)
                    
            
 
    

                  
app.run(debug=True)