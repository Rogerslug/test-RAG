# src/classes/gptClass.py
import requests
import json

class GptService:
    def getGptEnv(env):
        try:
            print("Ejecutando método 'getEnv' con GptController")
            with open('lib/gpt.json') as f:
                datas = json.load(f) # Cargar la configuración del modelo de lenguaje
                envi = datas[env]
                print(f"\nObteniendo la variable '{env}' con valor '{envi}'\n")
            return envi
        except Exception as e:
            print(f"Error al obtener el valor de la variable '{env}': {e}")
            raise Exception(f"Error al obtener el valor de la variable '{env}': {e}")

    """ Estructura de llamada al modelo de lenguaje:
    - Mensaje de sistema: Cómo el modelo de lenguaje va a comportarse
    - Mensaje del usuario: El mensaje que se el usuario quiere que el modelo de lenguaje responda 
    - temperatura: Control de la creatividad (0.0 como menos creativo, 1.0 como más creativo)
    - número máximo de tokens: Cantidad máxima de tokens a generar
    - modelo de lenguaje: El modelo de lenguaje a utilizar
    - endpoint de llamada al modelo de lenguaje: URL del endpoint al modelo de lenguaje
    - api_key de acceso al modelo de lenguaje: La clave de acceso al modelo de lenguaje
    """
    
    @staticmethod
    def gptEs(system, conversationHistory, temperature, token, model, endpoint, api_key): # Llamada al modelo de lenguaje
            try:
                print("Ejecutando método 'gptEs' desde clase")
                lang_es = GptService.getGptEnv('lenguaje_es')
                
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}'
                }
                # print(f"\nValores recuperados: \n 'Temperatura': {temperature}\n 'Modelo de lenguaje': {model}\n 'API key': {api_key}\n 'Endpoint de llamada al modelo de lenguaje': {endpoint}\n 'Token de longitud máxima': {token}\n 'Mensaje de sistema': {system}\n")
                # Llamada al modelo de lenguaje con el historial completo
                gptCompletion = requests.post(
                    endpoint, # URL del endpoint al modelo de lenguaje
                    headers=headers,
                    json={
                        "model": model, # Modelo de lenguaje a utilizar
                        "messages": [
                            {
                                "role": "system", # Tipo de mensaje (sistema)
                                "content": (system + lang_es) # Contenido del mensaje del sistema y el idioma
                            },
                            {
                                "role": "user", # Tipo de mensaje (usuario)
                                "content": (conversationHistory) # El historial de conversación ya contiene el nuevo mensaje del usuario
                            }
                        ],
                        "max_tokens": token, # Cantidad máxima de tokens a generar
                        "temperature": temperature # Control de la creatividad (0.0 como menos creativo, 1.0 como más creativo)
                    }
                ).json()
                # print(f"Respuesta del modelo de lenguaje desde GptService en GptClass.py: {gptCompletion}")
                return { "data": gptCompletion }
            except Exception as e:
                print('Error al procesar la solicitud, verifique su api_key o conexión a internet:', e)
                raise Exception('Error al procesar la solicitud, verifique su api_key o conexión a internet:', e)