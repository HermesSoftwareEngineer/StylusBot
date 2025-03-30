from flask import Flask
import os
from flask_cors import CORS

import sys
import os

# Adiciona o diretório src ao caminho do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = "dev",
        DATABASE = os.path.join(app.instance_path, 'stylusbot.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        return "<h2>Olá, Mundo!</h2>"
    
    from blueprints import messages
    app.register_blueprint(messages.bp)

    CORS(app, origins=['http://localhost:5173'])

    return app