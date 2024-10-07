# src/app.py
from flask import Flask
from routes.routes import route

app = Flask(__name__)
app.register_blueprint(route, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, port=5000)