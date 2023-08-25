import mysql.connector
from flask import Flask, request


connection = mysql.connector.connect(host='localhost', 
                                     database='work_flask',
                                     user='timotei',
                                     password='Timotei994')
cursor = connection.cursor()
 
class Client():
    def __init__(self, id, name, age, city):
        self.id = id
        self.name = name
        self.age = age
        self.city = city
        
app = Flask(__name__)


     #GET
@app.route("/client", methods = ['GET'])
def get():
    
    query = """SELECT * FROM client"""
    cursor.execute(query)
    curs = cursor.fetchall()
    return curs


    #POST
@app.route("/client", methods = ['POST'])
def post():
    
    client = Client(
        request.json['id'],
        request.json['name'],
        request.json['age'],
        request.json['city'],
    )
    
    value =(client.id, client.name, client.age, client.city,)
    command = """INSERT IGNORE INTO client (client.id, client.name, client.age, client.city) VALUES (%s, %s, %s, %s)""" 
    cursor.execute(command, value)
    connection.commit()
    return 'Method POST was successful'

    #PUT
@app.route("/client/<id>", methods = ['PUT'])
def put(id):

    client = Client(
        id,
        request.json['name'], 
        request.json['age'],
        request.json['city'],
    )

    value =(client.name, client.age, client.city, id)
    command = """UPDATE client SET name = %s, age = %s, city = %s WHERE id = %s""" 
    cursor.execute(command, value)
    connection.commit()
    return 'Method PUT was successful'

    #DELETE
@app.route("/client/<id>", methods = ['DELETE'])
def delete(id):
    
    value = (id, )
    command = """DELETE FROM client WHERE id = %s"""
    cursor.execute(command, value)
    connection.commit()
    return 'Method DELETE was successful'