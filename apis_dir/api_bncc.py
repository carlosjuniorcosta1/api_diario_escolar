from flask import Flask, jsonify, request 
import pyodbc
from flask_pydantic_spec import FlaskPydanticSpec

app = Flask(__name__)
spec = FlaskPydanticSpec('flask', title = "Endpoints da api de consulta \
                         da Base Nacional Curricular Comum - BNCC")
spec.register(app)

data_for_connection = (
    "Driver={SQL Server Native Client RDA 11.0};"
    "Server=DESKTOP-1698A6Q\SQLEXPRESS;"
    "Database=bncc;"  
    "Trusted_connection=YES;"
)

connection = pyodbc.connect(data_for_connection)
cursor = connection.cursor()


print("Abra o navegador e digite /apibncc após seu localhost")

show_table_names = cursor.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES \
                                  WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG='bncc'")
table_names = show_table_names.fetchall()

for x in table_names:
    print(x)


@app.route('/apibncc/<subject>', methods=["GET"])
@app.route('/apibncc/<subject>/<grade>', methods = ["GET"])
def list_all(subject, grade = None):
    """Lista todo o currículo por matéria e por ano via path, por matéria e/ou matéria e ano.
Escolha o currículo a ser consultado: \n
bncc_artes_ef \n
bncc_ciencias_ef \n
bncc_educacao_fisica_ef \n
bncc_ensino_religioso_ef \n 
bncc_geografia_ef \n
bncc_historia_ef \n
bncc_lingua_inglesa_ef \n
bncc_matematica_ef \n
bncc_lingua_portuguesa_ef \n

Escolha o ano a ser consultado: \n
Ensino fundamental: \n
sexto_ef \n 
setimo_ef \n 
oitavo_ef \n 
nono_ef \n

Ensino Médio:
primeiro_em \n
segundo_em \n
terceiro_em 
   
    """
    try:
        if len(grade) > 0:        
            db = cursor.execute(f"SELECT * FROM {subject} where {grade} = 'true'")
            data_get = db.fetchall()
            data_show = []
            if subject == "bncc_lingua_portuguesa_ef":
                pl_list = []
                for x in data_get:
                    pl_list.append({
                    "column1" : x[0],
                    "componente": x[1],
                    'ano_faixa': x[2],
                    'campo_atuacao': x[3],
                    'praticas_linguagem': x[4],
                    'objetos_conhecimento': x[5],
                    'habilidades': x[6],
                    'cod_hab': x[7],
                    'descricao_cod': x[8],
                    'primeiro_ef': x[9],
                    'segundo_ef': x[10],
                    'terceiro_ef': x[11],
                    'quarto_ef': x[12],
                    'quinto_ef': x[13],
                    'sexto_ef': x[14],
                    'setimo_ef': x[15],
                    'oitavo_ef': x[16],
                    'nono_ef': x[17]
                })
                return jsonify(message = "Dados solicitados", data = pl_list)
            elif subject == "bncc_lingua_inglesa_ef":
                eng_list = []
                for x in data_get:
                    eng_list.append({
                'column1': x[0],
                'componente': x[1], 
                'ano_faixa': x[2], 
                'eixo': x[3], 
                'unidades_tematicas': x[4],                    
                'objetos_conhecimento': x[5], 
                'habilidades': x[6],
                'cod_hab': x[7],
                'descricao_cod': x[8],                
                'primeiro_ef': x[9],
                'segundo_ef': x[10],
                'terceiro_ef': x[11],
                'quarto_ef': x[12], 
                'quinto_ef': x[13],
                
                'sexto_ef': x[14], 
                'setimo_ef': x[15], 
                'oitavo_ef': x[16], 
                'nono_ef': x[17]
                })
                return jsonify(message = "dados", data = eng_list)
            elif subject.endswith("_ef") and subject not in ["bncc_lingua_portuguesa_ef", "bncc_lingua_inglesa_ef"]:
                for x in data_get:
                    data_show.append({
                    'column1': x[0],
                    'componente': x[1],
                    'ano_faixa' : x[2],
                    'objetos_conhecimento': x[3],
                    'unidades_tematicas': x[4],
                    'habilidades': x[5],
                    'cod_hab': x[6], 
                    'descricao_cod': x[7], 
                    'primeiro_ef': x[8], 
                    'segundo_ef':x[9], 
                    'terceiro_ef': x[10],
                    'quarto_ef': x[11],
                    'quinto_ef': x[12],
                    'sexto_ef': x[13],
                    'setimo_ef': x[14],
                    'oitavo_ef': x[15],
                    'nono_ef': x[16]
                })
                return jsonify(message= "dados", data = data_show)
            elif subject.endswith("_inf") and not subject.startswith("df"):
                inf_list = []
                for x in data_get:
                    inf_list.append({
                        "column1": x[0],
                        "campo_exp": x[1],
                        "faixa_etaria": x[2],
                        "obj": x[3],
                        "cod_apr": x[4],
                        "descricao_cod": x[5],
                        "idade_anos_inicial": x[6],
                        "idade_meses_inicial": x[7],
                        "idade_anos_final": x[8],
                        "idade_meses_final": x[9]

                    })
                return jsonify(message = "Esses são os dados solicitados", data = inf_list)
            elif subject == "df_edu_inf":
                df_edu_inf_list = []
                for x in data_get:
                        df_edu_inf_list.append({
                        "column1": x[0],
                        "campo_exp": x[1],
                        "faixa_etaria": x[2],
                        "cod_apr": x[3],
                        "descricao_cod": x[4],
                        "idade_anos_inicial": x[5],
                        "idade_meses_inicial": x[6],
                        "idade_anos_final": x[7],
                        "idade_meses_final": x[8]
                        })
                return jsonify(message = "Esses são os dados solicitados do df_edu_inf", data = df_edu_inf_list)
            elif subject.endswith("_em") and not subject.startswith("c"):
                em_list = []
                for x in data_get:
                    em_list.append({                   
                        'column1': x[0],
                        'ano_faixa': x[1], 
                        'cod_hab': x[2],
                        'habilidades': x[3],
                        'primeiro_ano': x[4],
                        'segundo_ano': x[5],
                        'terceiro_ano': x[6],
                        'area': x[7], 
                        'competencias_esp': x[8],
                        'campos_atuacao' : x[9]
                    })
                return jsonify(message = "Dados de df_habilidades_em", data = em_list)
            elif subject.endswith("_em") and subject.startswith("c"):
                em_competencias_list = []
                for x in data_get:
                    em_competencias_list.append({
                        "column1": x[0],
                        "competencias": x[1],
                        "area": x[2]
                    })
                return jsonify(message = "Dados solicitados", data = em_competencias_list)
    except:
        if grade == None:
            db = cursor.execute(f"SELECT * FROM {subject}")
            data_get = db.fetchall()
            data_show = []
            if subject == "bncc_lingua_portuguesa_ef":
                pl_list = []
                for x in data_get:
                    pl_list.append({
                    "column1" : x[0],
                    "componente": x[1],
                    'ano_faixa': x[2],
                    'campo_atuacao': x[3],
                    'praticas_linguagem': x[4],
                    'objetos_conhecimento': x[5],
                    'habilidades': x[6],
                    'cod_hab': x[7],
                    'descricao_cod': x[8],
                    'primeiro_ef': x[9],
                    'segundo_ef': x[10],
                    'terceiro_ef': x[11],
                    'quarto_ef': x[12],
                    'quinto_ef': x[13],
                    'sexto_ef': x[14],
                    'setimo_ef': x[15],
                    'oitavo_ef': x[16],
                    'nono_ef': x[17]
                })
                return jsonify(message = "Dados solicitados", data = pl_list)
            elif subject == "bncc_lingua_inglesa_ef":
                eng_list = []
                for x in data_get:
                    eng_list.append({
                'column1': x[0],
                'componente': x[1], 
                'ano_faixa': x[2], 
                'eixo': x[3], 
                'unidades_tematicas': x[4],                    
                'objetos_conhecimento': x[5], 
                'habilidades': x[6],
                'cod_hab': x[7],
                'descricao_cod': x[8],                
                'primeiro_ef': x[9],
                'segundo_ef': x[10],
                'terceiro_ef': x[11],
                'quarto_ef': x[12], 
                'quinto_ef': x[13],
                
                'sexto_ef': x[14], 
                'setimo_ef': x[15], 
                'oitavo_ef': x[16], 
                'nono_ef': x[17]
                })
                return jsonify(message = "dados", data = eng_list)
            elif subject.endswith("_ef") and subject not in ["bncc_lingua_portuguesa_ef", "bncc_lingua_inglesa_ef"]:
                for x in data_get:
                    data_show.append({
                    'column1': x[0],
                    'componente': x[1],
                    'ano_faixa' : x[2],
                    'unidades_tematicas': x[3],
                    'objetos_conhecimento': x[4],
                    'habilidades': x[5],
                    'cod_hab': x[6], 
                    'descricao_cod': x[7], 
                    'primeiro_ef': x[8], 
                    'segundo_ef':x[9], 
                    'terceiro_ef': x[10],
                    'quarto_ef': x[11],
                    'quinto_ef': x[12],
                    'sexto_ef': x[13],
                    'setimo_ef': x[14],
                    'oitavo_ef': x[15],
                    'nono_ef': x[16]
                })
                return jsonify(message= "dados", data = data_show)
            elif subject.endswith("_inf") and not subject.startswith("df"):
                inf_list = []
                for x in data_get:
                    inf_list.append({
                        "column1": x[0],
                        "campo_exp": x[1],
                        "faixa_etaria": x[2],
                        "obj": x[3],
                        "cod_apr": x[4],
                        "descricao_cod": x[5],
                        "idade_anos_inicial": x[6],
                        "idade_meses_inicial": x[7],
                        "idade_anos_final": x[8],
                        "idade_meses_final": x[9]

                    })
                return jsonify(message = "Esses são os dados solicitados", data = inf_list)
            elif subject == "df_edu_inf":
                df_edu_inf_list = []
                for x in data_get:
                        df_edu_inf_list.append({
                        "column1": x[0],
                        "campo_exp": x[1],
                        "faixa_etaria": x[2],
                        "cod_apr": x[3],
                        "descricao_cod": x[4],
                        "idade_anos_inicial": x[5],
                        "idade_meses_inicial": x[6],
                        "idade_anos_final": x[7],
                        "idade_meses_final": x[8]
                        })
                return jsonify(message = "Esses são os dados solicitados do df_edu_inf", data = df_edu_inf_list)
            elif subject.endswith("_em") and not subject.startswith("c"):
                em_list = []
                for x in data_get:
                    em_list.append({                   
                        'column1': x[0],
                        'ano_faixa': x[1], 
                        'cod_hab': x[2],
                        'habilidades': x[3],
                        'primeiro_ano': x[4],
                        'segundo_ano': x[5],
                        'terceiro_ano': x[6],
                        'area': x[7], 
                        'competencias_esp': x[8],
                        'campos_atuacao' : x[9]
                    })
                return jsonify(message = "Dados de df_habilidades_em", data = em_list)
            elif subject.endswith("_em") and subject.startswith("c"):
                em_competencias_list = []
                for x in data_get:
                    em_competencias_list.append({
                        "column1": x[0],
                        "competencias": x[1],
                        "area": x[2]
                    })
                return jsonify(message = "Dados solicitados", data = em_competencias_list)


@app.route('/apibncc/', methods = ["GET"])
def list_all_two():
    """Lista todo o currículo por matéria e ano via query string"""
    subject = request.args.get('materia', None, type= str)
    grade = request.args.get('ano', None, type = str)
                          
    try:
        if len(grade) > 0:        
            db = cursor.execute(f"SELECT * FROM {subject} where {grade} = 'true'")
            data_get = db.fetchall()
            data_show = []
            if subject == "bncc_lingua_portuguesa_ef":
                pl_list = []
                for x in data_get:
                    pl_list.append({
                    "column1" : x[0],
                    "componente": x[1],
                    'ano_faixa': x[2],
                    'campo_atuacao': x[3],
                    'praticas_linguagem': x[4],
                    'objetos_conhecimento': x[5],
                    'habilidades': x[6],
                    'cod_hab': x[7],
                    'descricao_cod': x[8],
                    'primeiro_ef': x[9],
                    'segundo_ef': x[10],
                    'terceiro_ef': x[11],
                    'quarto_ef': x[12],
                    'quinto_ef': x[13],
                    'sexto_ef': x[14],
                    'setimo_ef': x[15],
                    'oitavo_ef': x[16],
                    'nono_ef': x[17]
                })
                return jsonify(message = "Dados solicitados", data = pl_list)
            elif subject == "bncc_lingua_inglesa_ef":
                eng_list = []
                for x in data_get:
                    eng_list.append({
                'column1': x[0],
                'componente': x[1], 
                'ano_faixa': x[2], 
                'eixo': x[3], 
                'unidades_tematicas': x[4],                    
                'objetos_conhecimento': x[5], 
                'habilidades': x[6],
                'cod_hab': x[7],
                'descricao_cod': x[8],                
                'primeiro_ef': x[9],
                'segundo_ef': x[10],
                'terceiro_ef': x[11],
                'quarto_ef': x[12], 
                'quinto_ef': x[13],
                
                'sexto_ef': x[14], 
                'setimo_ef': x[15], 
                'oitavo_ef': x[16], 
                'nono_ef': x[17]
                })
                return jsonify(message = "dados", data = eng_list)
            elif subject.endswith("_ef") and subject not in ["bncc_lingua_portuguesa_ef", "bncc_lingua_inglesa_ef"]:
                for x in data_get:
                    data_show.append({
                    'column1': x[0],
                    'componente': x[1],
                    'ano_faixa' : x[2],
                    'objetos_conhecimento': x[3],
                    'unidades_tematicas': x[4],
                    'habilidades': x[5],
                    'cod_hab': x[6], 
                    'descricao_cod': x[7], 
                    'primeiro_ef': x[8], 
                    'segundo_ef':x[9], 
                    'terceiro_ef': x[10],
                    'quarto_ef': x[11],
                    'quinto_ef': x[12],
                    'sexto_ef': x[13],
                    'setimo_ef': x[14],
                    'oitavo_ef': x[15],
                    'nono_ef': x[16]
                })
                return jsonify(message= "dados", data = data_show)
            elif subject.endswith("_inf") and not subject.startswith("df"):
                inf_list = []
                for x in data_get:
                    inf_list.append({
                        "column1": x[0],
                        "campo_exp": x[1],
                        "faixa_etaria": x[2],
                        "obj": x[3],
                        "cod_apr": x[4],
                        "descricao_cod": x[5],
                        "idade_anos_inicial": x[6],
                        "idade_meses_inicial": x[7],
                        "idade_anos_final": x[8],
                        "idade_meses_final": x[9]

                    })
                return jsonify(message = "Esses são os dados solicitados", data = inf_list)
            elif subject == "df_edu_inf":
                df_edu_inf_list = []
                for x in data_get:
                        df_edu_inf_list.append({
                        "column1": x[0],
                        "campo_exp": x[1],
                        "faixa_etaria": x[2],
                        "cod_apr": x[3],
                        "descricao_cod": x[4],
                        "idade_anos_inicial": x[5],
                        "idade_meses_inicial": x[6],
                        "idade_anos_final": x[7],
                        "idade_meses_final": x[8]
                        })
                return jsonify(message = "Esses são os dados solicitados do df_edu_inf", data = df_edu_inf_list)
            elif subject.endswith("_em") and not subject.startswith("c"):
                em_list = []
                for x in data_get:
                    em_list.append({                   
                        'column1': x[0],
                        'ano_faixa': x[1], 
                        'cod_hab': x[2],
                        'habilidades': x[3],
                        'primeiro_ano': x[4],
                        'segundo_ano': x[5],
                        'terceiro_ano': x[6],
                        'area': x[7], 
                        'competencias_esp': x[8],
                        'campos_atuacao' : x[9]
                    })
                return jsonify(message = "Dados de df_habilidades_em", data = em_list)
            elif subject.endswith("_em") and subject.startswith("c"):
                em_competencias_list = []
                for x in data_get:
                    em_competencias_list.append({
                        "column1": x[0],
                        "competencias": x[1],
                        "area": x[2]
                    })
                return jsonify(message = "Dados solicitados", data = em_competencias_list)
    except:
        if grade == None:
            db = cursor.execute(f"SELECT * FROM {subject}")
            data_get = db.fetchall()
            data_show = []
            if subject == "bncc_lingua_portuguesa_ef":
                pl_list = []
                for x in data_get:
                    pl_list.append({
                    "column1" : x[0],
                    "componente": x[1],
                    'ano_faixa': x[2],
                    'campo_atuacao': x[3],
                    'praticas_linguagem': x[4],
                    'objetos_conhecimento': x[5],
                    'habilidades': x[6],
                    'cod_hab': x[7],
                    'descricao_cod': x[8],
                    'primeiro_ef': x[9],
                    'segundo_ef': x[10],
                    'terceiro_ef': x[11],
                    'quarto_ef': x[12],
                    'quinto_ef': x[13],
                    'sexto_ef': x[14],
                    'setimo_ef': x[15],
                    'oitavo_ef': x[16],
                    'nono_ef': x[17]
                })
                return jsonify(message = "Dados solicitados", data = pl_list)
            elif subject == "bncc_lingua_inglesa_ef":
                eng_list = []
                for x in data_get:
                    eng_list.append({
                'column1': x[0],
                'componente': x[1], 
                'ano_faixa': x[2], 
                'eixo': x[3], 
                'unidades_tematicas': x[4],                    
                'objetos_conhecimento': x[5], 
                'habilidades': x[6],
                'cod_hab': x[7],
                'descricao_cod': x[8],                
                'primeiro_ef': x[9],
                'segundo_ef': x[10],
                'terceiro_ef': x[11],
                'quarto_ef': x[12], 
                'quinto_ef': x[13],
                
                'sexto_ef': x[14], 
                'setimo_ef': x[15], 
                'oitavo_ef': x[16], 
                'nono_ef': x[17]
                })
                return jsonify(message = "dados", data = eng_list)
            elif subject.endswith("_ef") and subject not in ["bncc_lingua_portuguesa_ef", "bncc_lingua_inglesa_ef"]:
                for x in data_get:
                    data_show.append({
                    'column1': x[0],
                    'componente': x[1],
                    'ano_faixa' : x[2],
                    'unidades_tematicas': x[3],
                    'objetos_conhecimento': x[4],
                    'habilidades': x[5],
                    'cod_hab': x[6], 
                    'descricao_cod': x[7], 
                    'primeiro_ef': x[8], 
                    'segundo_ef':x[9], 
                    'terceiro_ef': x[10],
                    'quarto_ef': x[11],
                    'quinto_ef': x[12],
                    'sexto_ef': x[13],
                    'setimo_ef': x[14],
                    'oitavo_ef': x[15],
                    'nono_ef': x[16]
                })
                return jsonify(message= "dados", data = data_show)
            elif subject.endswith("_inf") and not subject.startswith("df"):
                inf_list = []
                for x in data_get:
                    inf_list.append({
                        "column1": x[0],
                        "campo_exp": x[1],
                        "faixa_etaria": x[2],
                        "obj": x[3],
                        "cod_apr": x[4],
                        "descricao_cod": x[5],
                        "idade_anos_inicial": x[6],
                        "idade_meses_inicial": x[7],
                        "idade_anos_final": x[8],
                        "idade_meses_final": x[9]

                    })
                return jsonify(message = "Esses são os dados solicitados", data = inf_list)
            elif subject == "df_edu_inf":
                df_edu_inf_list = []
                for x in data_get:
                        df_edu_inf_list.append({
                        "column1": x[0],
                        "campo_exp": x[1],
                        "faixa_etaria": x[2],
                        "cod_apr": x[3],
                        "descricao_cod": x[4],
                        "idade_anos_inicial": x[5],
                        "idade_meses_inicial": x[6],
                        "idade_anos_final": x[7],
                        "idade_meses_final": x[8]
                        })
                return jsonify(message = "Esses são os dados solicitados do df_edu_inf", data = df_edu_inf_list)
            elif subject.endswith("_em") and not subject.startswith("c"):
                em_list = []
                for x in data_get:
                    em_list.append({                   
                        'column1': x[0],
                        'ano_faixa': x[1], 
                        'cod_hab': x[2],
                        'habilidades': x[3],
                        'primeiro_ano': x[4],
                        'segundo_ano': x[5],
                        'terceiro_ano': x[6],
                        'area': x[7], 
                        'competencias_esp': x[8],
                        'campos_atuacao' : x[9]
                    })
                return jsonify(message = "Dados de df_habilidades_em", data = em_list)
            elif subject.endswith("_em") and subject.startswith("c"):
                em_competencias_list = []
                for x in data_get:
                    em_competencias_list.append({
                        "column1": x[0],
                        "competencias": x[1],
                        "area": x[2]
                    })
                return jsonify(message = "Dados solicitados", data = em_competencias_list)
    
app.run(debug=True)
   

    




