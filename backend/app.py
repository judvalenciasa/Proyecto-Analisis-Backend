from flask import Flask, request, jsonify #Microframework para facilitar el desarrollo de app web
import psycopg2 #Apartard de bd postgreSQL
from flask_cors import CORS #Permite obtener permiso para acceder a recursos de un servidor

app = Flask(__name__)

#Conexión a la base de datos
def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='postgres',
                            user='postgres',
                            password='12345',
                            port=5433)
    return conn
CORS(app)

#Método de prueba
@app.route('/')
def index():
    return '<h1>HELLO</h1>'

#Método para cuardar la informaciónde un grafo en la base de datos
@app.route('/grafos', methods=['POST'])
def create():
    conn = get_db_connection()
    cur = conn.cursor()
    nombre = request.json['nombre']
    grafo = request.json['grafo']
    cur.execute('INSERT INTO grafos_analisis (nombre, grafo)'
                'VALUES (%s, %s)',
                (nombre, grafo))
    conn.commit()
    cur.close()
    conn.close()
    return "OK"

#Retorna la información de la base de datos
@app.route('/grafos', methods=['GET', 'OPTIONS', 'Access-Control-Allow-Methods'])
def getGrafos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM grafos_analisis;')
    grafos = cur.fetchall()
    cur.close()
    conn.close()
    print(grafos)
    return jsonify(grafos)

if __name__ == "__main__":
    app.run(debug=True)

