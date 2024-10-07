# Proyecto RAG

## Descripción

El proyecto consiste en la creación de un sistema de RAGs (Retrieval Augmented Generation) que utiliza modelos de lenguaje de alto rendimiento y una base de datos de alta calidad para generar descripciones de productos y servicios. El sistema se basa en modelos de lenguaje de ejecución local y una base de datos MariaDB.

## Tecnologías

- Python
- Flask
- MariaDB
- MySQL
- LM-Studio
- PHI-3.5
- Llama 3.2 (Modelo de lenguaje pequeño, ideal para ejecución local)

## Estructura del proyecto

```
.
├── lib
│   ├── config.json
│   ├── gpt.json
├── src
│   ├── app.py
│   ├── classes
│   │   ├── gptClass.py
│   │   ├── sqlClass.py
│   ├── controllers
│   │   ├── gptController.py
│   │   ├── sqlController.py
│   ├── routes
│   │   ├── routes.py

``` Estas carpetas se encuentran en la carpeta raíz del proyecto

## Ejecución del proyecto

### Requerimientos

1. Python 3.10.6
2. MariaDB ejecutando en localhost (En este caso desde un servicio de máquina virtual con CentOS)
3. Lm-Studio para ejecutar el modelo de lenguaje en el entorno local
4. Levantar el servidor donde se ejecutará el modelo de lenguaje en Lm-Studio
4.1. PHI-3.5 instalado y ejecutando en Lm-Studio como servidor (Opcional)
4.2. Llama 3.2 instalado y ejecutando en Lm-Studio como servidor (Opcional)
5. Postman para ejecutar las peticiones HTTP

### Instalación

1. Clonar el repositorio en tu máquina
2. Abrir una terminal en la carpeta raíz del proyecto
3. Ejecutar el siguiente comando para inicializar el entorno virtual e instalar las dependencias:
    ```
    ./setup.ps1
    ```
4. Ejecutar el siguiente comando para iniciar el servidor de Flask:
    python ./src/app.py
5. Abrir Lm-Studio, buscar en la lista de modelos de lenguajo PHI-3.5, descargar el modelo y cargarlo en el entorno local
6. En Lm-Studio, dirigirse a la sección de "Desarrollador", definir el puerto del localhost a 5001 y levantar el servidor
7. En la máquina virtual con CentOS, abrir una terminal y ejecutar el siguiente comando para comenzar a instalar el servidor de MariaDB y ejecutar la base de datos:
    ```
    yum update
    yum install MariaDB
    systemctl start mariadb
    systemctl enable mariadb
    ```
8. En la máquina virtual con CentOS, importar la base de datos desde el repositorio "Infiltrautos" en una carpeta de Centos personalizada, de preferencia llamada "Infiltrautos"
8.1 NOTA: Si no está instalado el comando unzip y wget, ejecutar el siguiente comando para instalarlos:
    ```
    yum install unzip wget
    ```
8.2 Ya dentro de la carpeta de la base de datos, ejecutar el siguiente comando para descargar los archivos de la base de datos:
    ```
    wget https://github.com/Rogerslug/InfiltrautosDB/archive/refs/heads/main.zip
    ```
9. Descomprimir el archivo descargado:
    ```
    unzip main.zip
    ```
10. Una vez descomprimido, ejecutar los siguientes comandos para importar las siguientes tablas de la base de datos: 
    ```
    mysql -u root -p <  auto.sql
    mysql -u root -p <  filters.sql
    mysql -u root -p <  users.sql
    ```
11. Para importar los datos de la base de datos, ejecutar los siguientes comandos igualmente en orden:
    ```
    mysql -u root -p <  autodata.sql
    mysql -u root -p <  filtersdata.sql
    ```
12. Preparar la base de datos para la conexión desde la maquina virtual con CentOS al entorno local de Flask ejecutándose en windows:
    
12.1 Revisar la dirección IP de la máquina virtual con CentOS en el archivo de configuración de la base de datos:
    ```
    ip addr
    ``` Esto mostrará la dirección IP de la máquina virtual con CentOS en el archivo de configuración de la base de datos.

12.2 Copiar la dirección IP de la máquina virtual con CentOS en el archivo de configuración de la base de datos, normalmente este valor se encuentra en el segundo adaptador de red de la máquina virtual con CentOS en el campo inet:
    ```
    inet 192.168.1.73/24 brd 192.168.1.255 scope global dynamic noprefixroute eth0 [Este es solo un ejemplo, en este caso se copia la dirección IP 192.168.1.73]
    ```

12.3 Pegar la dirección IP al archivo ./src/classes/sqlClass.py en el método connect() en la siguiente sección:
    ```
    self.connection = mysql.connector.connect(
        host='192.168.1.73', 
        user='root', 
        password=password, 
        database='Infiltrautos') # Guardar los cambios
    ```
13. Iniciar Postman y crear una nueva sección donde se ejecuten las peticiones HTTP para InfiltrautosDB

13.1 http://localhost:5000/api/test GET, para comprobar con un SHOW TABLES que se obtienen las bases de datos correctamente al servidor de la base de datos

    json esperado:
    {
    "code": 200,
    "data": [
        "Autos",
        "Filtros",
        "Usuarios"
    ],
    "message": "Conexión exitosa a la BD, bases de datos obtenidas",
    "ok": true
    }

13.2 http://localhost:5000/api/testGPT POST, para comprobar que el servidor junto con la base de datos y el modelo de lenguaje está funcionando correctamente

    josn requerido:
    {
        "message": "Hola, preséntate"
    }

    json esperado:
    {
        "code": 200,
        "data": {
            "code": 200,
            "data": {
                "choices": [
                    {
                        "finish_reason": "stop",
                        "index": 0,
                        "logprobs": null,
                        "message": {
                            "content": "¡Hola! Me alegra que hayas decidido hablar conmigo. Mi nombre es Llama, y estoy aquí para ayudarte con cualquier pregunta o tema que te guste. ¿En qué puedo ayudarte hoy?",
                            "role": "assistant"
                        }
                    }
                ],
                "created": 1727567410,
                "id": "chatcmpl-mu1338x4zbuawqo9muc0r",
                "model": "NikolayKozloff/Llama-3.2-1B-Instruct-Q8_0-GGUF/llama-3.2-1b-instruct-q8_0.gguf",
                "object": "chat.completion",
                "system_fingerprint": "NikolayKozloff/Llama-3.2-1B-Instruct-Q8_0-GGUF/llama-3.2-1b-instruct-q8_0.gguf",
                "usage": {
                    "completion_tokens": 46,
                    "prompt_tokens": 72,
                    "total_tokens": 118
                }
            },
            "message": "Respuesta exitosa",
            "ok": true
        },
        "message": "Respuesta exitosa",
        "ok": true
    }

    NOTA: Se debe corregir la manera de obtener el resultado de la consulta, ya que se hace redundante el arquetipo de la consulta y el resultado de la consulta.

13.3 http://localhost:5000/api/querySql POST, para comprobar que se ejecuten las consultas SQL correctamente al servidor de la base de datos

    json requerido:
    {
    "query": "SELECT * FROM Filtros;"
    }

    json esperado:
    {
    "code": 200,
    "data": [
        [
            1,
            "Filtro de Aire Fram CA8007",
            "Fibra Sintetica",
            100,
            "1 Filtro de Aire Fram CA8007.jpg",
            70,
            "Rectangular",
            "1"
        ],
        [
            2,
            "Filtro de Aire Fram CA10217",
            "Fibra Sintetica",
            100,
            "2 Filtro de Aire Fram CA10217.avif",
            74,
            "Cilindrico",
            "2"
        ],...
    ],
    "message": "Query exitosa",
    "ok": true
}

13.4 http://localhost:5000/api/getFilters GET, para comprobar que se obtienen los filtros correctamente al servidor de la base de datos desde un query harcodeado

    json esperado:
    {
    "code": 200,
    "data": [
        [
            1,
            "Filtro de Aire Fram CA8007",
            "Fibra Sintetica",
            100,
            "1 Filtro de Aire Fram CA8007.jpg",
            70,
            "Rectangular",
            "1"
        ],...
    ],
    "message": "Obteniendo filtros",
    "ok": true
}

13.5 http://localhost:5000/api/testRag POST, para comprobar que se ejecuten las consultas SQL y llamadas al modelo de lenguaje correctamente al servidor del modelo de lenguaje 

    json requerido:
    {
        "message": "Se ve interesante este filtro",
        "temperature": "temperature_very_strict",
        "system": "system_assistant",
        "token": "max_tokens_medium",
        "model": "model_local",
        "endpoint": "endpoint_LLM_local",
        "api_key": "api_key_local"
    }

    json esperado: