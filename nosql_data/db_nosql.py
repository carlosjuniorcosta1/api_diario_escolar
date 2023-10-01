import pymongo

client = pymongo.MongoClient("mongodb://localhost", 27017)

#acessa o db al_db, que foi feito no mongodbCompass, importando um json feito no python
db = client["al_db"] 

collection = db["dados"]

def list_all_students():
        all_students = []
        for x in collection.find():
                all_students.append(x)
        
        return all_students, print(all_students)


def list_student_by_name(name: str):
        name_st = name
        query1 = {"nome": name_st }
        q1 = collection.find(query1)
        name_st_l = []               
        for x in q1:
                name_st_l.append(x)
        return name_st_l, print(name_st_l)
        
list_student_by_name('Kristian')
                

def insert_new_student(new_st):
        add_new = collection.insert_one(new_st)
        return print(add_new.inserted_id)

new_st = {"nome": "novo aluno", 'turma': 'sexto_ef', 'sobrenome': 'sobrenome do aluno'}
        
insert_new_student(new_st)
    
        
        
        
        
           
        




# Atualize um documento na coleção.
#collection.update_one({"name": "John"}, {"$set": {"age": 31}})

# Consulte novamente para verificar a atualização.
#updated_result = collection.find_one({"name": "John"})
#print(updated_result)

# Exclua um documento na coleção.
#collection.delete_one({"name": "John"})

# Certifique-se de fechar a conexão quando terminar.
client.close()
