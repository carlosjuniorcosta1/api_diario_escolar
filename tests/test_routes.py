from flask import Flask 
import json
import pytest
from flask.testing import FlaskClient

#testes unitários na api_alunos

from apis_dir.api_alunos import app
@pytest.fixture
def client() -> FlaskClient:
    app.testing = True
    return app.test_client()
    

def test_get_student(client):
    response = client.get('/diario/aluno/1')    
    
    assert response.status_code == 200
    
    
def test_get_all_students(client):
    response = client.get('/diario')    
    
    assert response.status_code == 200

def test_insert_student(client):
    response = client.post('/diario/inserir')    
    
    assert response.status_code == 200
    
    
def test_get_json_student(client):
    response = client.get('/diario/aluno/1')
    expected_json = {
  "data": [
    {
      "ano": "sexto",
      "cpf": "72776291812",
      "idade": 11,
      "nivel_ensino": "ef",
      "nome": "Brooke",
      "nome_completo": "Brooke Henderson",
      "sobrenome": "Henderson",
      "turma": 1
    }
  ],
  "message": "Aluno solicitado"
}
    assert response.json == expected_json
    
#por enquanto, o teste abaixo falhou porque o id_aluno também é uma chave estrangeira na tabela de notas
#em breve, veremos como solucionar isso
def test_delete_student_by_id(client):
    response = client.delete('diario/deletar/2')
    assert response.status_code == 204

    
    
    
  