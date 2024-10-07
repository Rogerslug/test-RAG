# src/controllers/gptController.py
from flask import request, jsonify
from werkzeug.exceptions import BadRequestKeyError
from classes.gptClass import GptService
import requests
import json

# Inicializar la variable acumulativa para la historia
conversationHistory = "" # historia de conversación acumulado en una sola cadena

class gptCtrl:
    def getGptEnv(env):
        try:
            print("Ejecutando método 'getEnv' con GptController")
            with open('lib/gpt.json') as f:
                datas = json.load(f) # Cargar la configuración de la API del modelo de lenguaje
                envi = datas[env]
                # print(f"\nObteniendo la variable '{env}' con valor '{envi}'\n")
            return envi
        except Exception as e:
            print(f"Error al obtener el valor de la variable '{env}': {e}")
            raise Exception(f"Error al obtener el valor de la variable '{env}': {e}")

    def testGpt():
        global conversationHistory # Permitir modificar la variable global
        try:
            print("Ejecutando método 'testGpt' con GptController")
            data = request.get_json()
            message = data['message']
            # print("Mensaje enviado: ", message, "\n")
            
            temperature = int(gptCtrl.getGptEnv('temperature_very_strict'))
            system = gptCtrl.getGptEnv('system_infiltrautos')
            token = int(gptCtrl.getGptEnv('max_tokens_medium'))
            model = gptCtrl.getGptEnv('model_local_llama')
            endpoint = gptCtrl.getGptEnv('endpoint_LLM_local')
            api_key = gptCtrl.getGptEnv('api_key_local')
            
            print("\nValores recuperados desde gptCtrl.testGpt: \n")
            print("Temperatura: ", temperature, "\n")
            print("Modelo de lenguaje: ", model, "\n")
            print("API key: ", api_key, "\n")
            print("Endpoint de llamada al modelo de lenguaje: ", endpoint, "\n")
            print("Token de longitud máxima: ", token, "\n")
            print("Mensaje enviado: ", message, "\n")
            
            # Concatenar la historia de conversación en una sola cadena
            conversationHistory += f"Usuario: {message}\n"
            
            # print("\nEjecutando método gptEn desde GptController")
            # Llamada al modelo de lenguaje
            callLlm = GptService.gptEs(system, conversationHistory, temperature, token, model, endpoint, api_key)
            
            # Concatenar la respuesta del modelo de lenguaje al historial de conversación
            conversationHistory += f"GPT: {callLlm['data']['choices'][0]['message']['content']}\n"
            
            print("Respuesta del modelo de lenguaje:", callLlm)
            return jsonify({ 
                "ok": True, 
                "message": "Respuesta exitosa", 
                "data": callLlm, 
                "code": 200
            }), 200
        except Exception as e:
            print(f"Error al llamar al modelo de lenguaje: {e}")
            return jsonify({ "ok": False, "message": f"Error al llamar al modelo de lenguaje", "data": f"{e}", "code": 500 }), 500

# Este método 
    def testRag(message, temperature, system, token, model, endpoint, api_key):
        # El modelo recibirá el mensaje del usuario y el resultado de la consulta a la base de datos
        global conversationHistory # Permitir modificar la variable global
        try:
            print("Ejecutando método 'testRag' con GptController")
            userMessage = message
            # print("Mensaje enviado: ", userMessage, "\n")
            temp = int(gptCtrl.getGptEnv(temperature))
            sys = gptCtrl.getGptEnv(system)
            tok = int(gptCtrl.getGptEnv(token))
            mod = gptCtrl.getGptEnv(model)
            end = gptCtrl.getGptEnv(endpoint)
            api = gptCtrl.getGptEnv(api_key)
            
            print(f"\nValores recuperados desde gptCtrl.testRag:\n 'Temperatura': {temp}\n 'Modelo de lenguaje': {mod}\n 'API key': {api}\n 'Endpoint de llamada al modelo de lenguaje': {end}\n 'Token de longitud máxima': {tok}\n 'Mensaje enviado': {userMessage}\n")
            
            # Concatenar la historia de conversación en una sola cadena
            conversationHistory += f"Usuario: {userMessage}\n"
            # print(f"Historial de conversación actualizado. gptCtrl.testRag: {conversationHistory}")
            
            # print("\nEjecutando método gptEs desde GptController")
            # Llamada al modelo de lenguaje
            callLlm = GptService.gptEs(sys, conversationHistory, temp, tok, mod, end, api)
            print(callLlm)
            
            # Concatenar la respuesta del modelo de lenguaje al historial de conversación
            conversationHistory += f"GPT: {callLlm['data']['choices'][0]['message']['content']}\n"
            print(f"Historial de conversación actualizado. {conversationHistory}")
            # print("Respuesta del modelo de lenguaje desde GptController.testRag:", callLlm)
            return { "data": callLlm['data']}
        except Exception as e:
            print(f"Error al llamar al modelo de lenguaje: {e}")
            return jsonify({ "ok": False, "message": f"Error al llamar al modelo de lenguaje", "data": f"{e}", "code": 500 }), 500
