from flask import request, jsonify
from werkzeug.exceptions import BadRequestKeyError
from classes.sqlClass import db_service
import requests
import json
from controllers.gptController import gptCtrl

class sqlCtrl:
    def getGptEnv(env):
        try:
            print("Ejecutando método 'getEnv' con GptController")
            with open('lib/gpt.json') as f:
                datas = json.load(f) # Cargar la configuración de la API del modelo de lenguaje
                envi = datas[env]
                print(f"\nObteniendo la variable '{env}' con valor '{envi}'\n")
            return envi
        except Exception as e:
            print(f"Error al obtener el valor de la variable '{env}': {e}")
            raise Exception(f"Error al obtener el valor de la variable '{env}': {e}")

    
    @staticmethod
    def test():
        try:
            print("Ejecutando método 'test'")
            connect = db_service.connect() # Conectar a la base de datos
            if connect is True:
                print("Conectado a MariaDb desde Controlador")
                print("True controller")
                query = "SHOW TABLES;"
                databases = db_service.execute_query(query) # Ejecutar el query 'SHOW DATABASES'
                
                if databases: # Validar si se obtuvo resultado
                    print(databases)
                    databases=[db[0] for db in databases] # Convertir el resultado a una lista de nombres de BD
                    print(f"Bases de datos obtenidas: {databases}")
                    return jsonify({ 
                        "ok": True, 
                        "message": "Conexión exitosa a la BD, bases de datos obtenidas", 
                        "data": databases,
                        "code": 200
                    }), 200
                else:
                    print("No se pudieron obtener las bases de datos")
                    return jsonify({ 
                        "ok": False, 
                        "message": "Error ejecutando el query", 
                        "data": None, 
                        "code": 500 
                    }), 500

            elif connect is False:
                print("Error al conectar a la bd desde controlador")
                print("False connect controller")
                return jsonify({ 
                    "ok": False, "message": f"Error al conectar a la BD", "data": None, "code": 500 }), 500
                
        except Exception as e:
            print(f"Error al conectar a la base de datos o ejecutar el query: {e}")
            return jsonify({ "ok": False, "message": f"Error al conectar a la BD o ejecutar el query", "data": f"{e}", "code": 500 }), 500
            
        finally: # Intentar cerrar la conexión
            close = db_service.disconnect()
            if close is True:
                print(f"{close} desde finally")
                print("Conexión a MariaDB cerrada correctamente desde controlador ")
            elif close is False:
                print(f"{close} desde finally")
                print("Conexión ya está cerrada")
                
    def gpt(system, message, temperature):
        try:
            with open('config.json') as f:
                datas = json.load(f)
                api_key = datas['api_key']
                
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }
            
            gptCompletion = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {
                            "role": "system",
                            "content": (system)
                        },
                        {
                            "role": "user",
                            "content": (message)
                        }
                    ],
                    "max_tokens": 1500,
                    "temperature": temperature
                }
            ).json()
            
        except Exception as e:
            print('Error al procesar la solicitud, verifique su api_key o conexión a internet:', e)
            return None
        
    def querySql():
        """ json esperado:
            {
                "query": "SELECT * FROM Filtros;"
            }
        """
        try:
            print("Ejecutando método 'querySql'")
            connect = db_service.connect() # Conectar a la base de datos
            if connect is True:
                print("Conectado a MariaDb desde Controlador")
                print("True controller")
                #Recuperar query desde el body
                query = request.get_json()
                print(query)
                
                query = query['query']
                print("Query: ", query)
                if query is None:
                    return jsonify({ "ok": False, "message": "Error en el body del request", "data": None, "code": 400 }), 400
                
                results = db_service.execute_query(query) # Ejecutar el query
                print("Resultados: ", results)
                if results: # Validar si se obtuvo resultado
                    print(results)
                    return jsonify({ "ok": True, "message": "Query exitosa", "data": results, "code": 200 }), 200
                else:
                    print("No se pudieron obtener los resultados")
                    return jsonify({ "ok": False, "message": "No se pudieron obtener los resultados", "data": None, "code": 500 }), 500
            elif connect is False:
                print("Error al conectar a la bd desde controlador")
                print("False connect controller")
                return jsonify({ "ok": False, "message": f"Error al conectar a la BD", "data": None, "code": 500 }), 500
        except Exception as e:
            print(f"Error al conectar a la base de datos o ejecutar el query: {e}")
            return jsonify({ "ok": False, "message": f"Error al conectar a la BD o ejecutar el query", "data": f"{e}", "code": 500 }), 500
        
    def getFilters():
        try:
            print("Ejecutando método 'getFilters'")
            connect = db_service.connect() # Conectar a la base de datos
            if connect is True:
                #print("Conectado a MariaDb desde Controlador")
                #print("True controller")
                # Get all filters
                query = "SELECT * FROM Filtros;"
                filters = db_service.execute_query(query) # Ejecutar el query
                
                if filters: # Validar si se obtuvo resultado
                    print(filters)
                    return jsonify({ "ok": True, "message": "Obteniendo filtros", "data": filters, "code": 200 }), 200
                else:
                    print("No se pudieron obtener los resultados")
                    return jsonify({ "ok": False, "message": "No se pudieron obtener los resultados", "data": None, "code": 500 }), 500
            elif connect is False:
                print("Error al conectar a la bd desde controlador")
                #print("False connect controller")
                return jsonify({ "ok": False, "message": f"Error al conectar a la BD", "data": None, "code": 500 }), 500
            
        except Exception as e:
            print(f"Error al conectar a la base de datos o ejecutar el query: {e}")
            return jsonify({ "ok": False, "message": f"Error al conectar a la BD o ejecutar el query", "data": f"{e}", "code": 500 }), 500
        finally: # Intentar cerrar la conexión
            close = db_service.disconnect()
            if close is True:
                #print(f"{close} desde finally")
                print("Conexión a MariaDB cerrada correctamente desde controlador ")
            elif close is False:
                #print(f"{close} desde finally")
                print("Conexión ya está cerrada")
                
    def testRag(): # Esta es una prueba de la interacción de GPT con el resultado de la consulta a la base de datos
            """ json esperado:
                {
                    "message": "y ocupo que me traiga la información que necesito",
                    "temperature": "temperature_very_strict",
                    "system": "system_assistant", # Darle al bot el conocimiento de que es un RAG
                    "token": "max_tokens_medium",
                    "model": "model_local",
                    "endpoint": "endpoint_LLM_local",
                    "api_key": "api_key_local"                    
                } 
            """
            try:
                print("Ejecutando método 'testRag'")
                data = request.get_json()
                #print(data)
                message = data['message']
                connect = db_service.connect() # Conectar a la base de datos
                if connect is True:
                    print("Conectado a MariaDb desde sqlCtrl.testRag")
                    
                    # Definir variables del json
                    message = data['message']
                    temperature = data['temperature']
                    system = data['system']
                    token = data['token']
                    model = data['model']
                    endpoint = data['endpoint']
                    api_key = data['api_key']
                    # print(f"\nValores recuperados desde testRag:\n 'Temperatura': {temperature}\n 'Modelo de lenguaje': {model}\n 'API key': {api_key}\n 'Endpoint de llamada al modelo de lenguaje': {endpoint}\n 'Token de longitud máxima': {token}\n 'Mensaje enviado': {message}\n")
                    
                    # Get all filters
                    queryDescribe = "DESCRIBE Filtros;"
                    querySelect = "SELECT * FROM Filtros WHERE id_filtro = 26;"
                    results = (f"Campos de la tabla: {db_service.execute_query(queryDescribe)}\n\nResultado de la consulta: {db_service.execute_query(querySelect)}")
                    # print(f"Resultado de la consulta: {results}")
                    
                    if results:                        
                        userMessage = f"\n\nMensaje del usuario: {message}\n\nQuery de consulta: {querySelect}\n\nResultado de las consultas: {results}"
                        # print(f"{userMessage}")
                        # llamar a testRag
                        callRag = gptCtrl.testRag(userMessage, temperature, system, token, model, endpoint, api_key)
                        """ ### Resultado del query y reultado del modelo de lenguaje """
                        # print(f"Resultado del modelo de lenguaje desde sqlCtrl.testRag: {callRag}")
                        if  results and callRag:
                            return jsonify({"ok": True, "message": "Respuesta exitosa", "data": callRag['data'], "code": 200}), 200
                        else:
                            print(f"[sqlCtrl.testRag] El modelo de lenguaje no devolvió resultados, devolviendo el resultado de la consulta")
                            return jsonify({ "ok": True, "message": "Modelo de lenguaje no devolvió resultados, devolviendo el resultado de la consulta", "data": results, "code": 200 }), 200
                    else:
                        print(f"[sqlCtrl.testRag] No se pudieron obtener los resultados de la consulta")
                        return jsonify({ "ok": False, "message": "No se pudieron obtener los resultados", "data": None, "code": 500 }), 500
                    
                else:
                    print(f"[sqlCtrl.testRag] No se pudo conectar a la base de datos")
                    return jsonify({ "ok": False, "message": "No se pudo conectar a la base de datos", "data": None, "code": 500 }), 500
            except Exception as e:
                print(f"Error en el servidor: {e}")
                print(f"[sqlCtrl.testRag] Error en el servidor: {e}")
                return jsonify({ "ok": False, "message": f"Error en el servidor", "data": None, "code": 500 }), 500
            