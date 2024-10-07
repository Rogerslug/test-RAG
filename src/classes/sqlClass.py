import mysql.connector
import json

with open('lib/config.json') as f:
    datas = json.load(f)
    password = datas['password']

class MariaDbService:
    def __init__(self): # Inicializa la clase   
        self.connection = None
        
    def connect(self): #Conexión a MariaDB en local
        try:
            self.connection = mysql.connector.connect(
                # host='192.168.1.73',
                host='192.168.43.17',
                user='root',
                password=password,
                database='Infiltrautos'
            )
            print("Conexión exitosa desde clase")
            active = True
            return active
        except mysql.connector.Error as e:
            print(f"Error al conectar a MariaDB desde clase: {e}")
            active = False
            return active

    def disconnect(self): # Cierra la conexión a la base de datos
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            close = True
            print("Conexión a MariaDB cerrada desde clase")
            return close
        else:
            close = False
            return close

    def execute_query(self, query): # Ejecuta una consulta SQL
        if self.connection.cursor is None or not self.connection.is_connected():
            print("No hay conexión establecida para ejecutar la consulta")
            raise Exception("No hay conexión a la base de datos")
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"Error ejecutando el query: {e}")
            raise Exception(f"Error al ejecutar el query: {e}")
        finally:
            cursor.close()
            
db_service = MariaDbService()