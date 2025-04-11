from flask import Blueprint, request
from src.bot.graph import app

bp = Blueprint('chat', __name__, url_prefix='/chat')

@bp.route('/index', methods=('GET', 'POST'))
def answer():
    if request.method == "POST":

        # Pegando o conteúdo do corpo
        data = request.get_json()    

        # Verificando a existência do thread_id    
        if data and 'thread_id' in data:
            thread_id = data['thread_id']
        else:
            return {"error": "thread_id is required!"}, 400
        
        # Verificando a existência do input do usuário
        if data and 'user_input' in data:
            user_input = data['user_input']
        else:
            return {"error": "user_input is required!"}, 400
        
        # Configurando para chamada do llm
        config = {'configurable': {'thread_id': thread_id}}

        # Chamando o llm
        response = app.invoke({'messages': user_input}, config)

        return {"resposta": response['messages'][-1].content}, 200

    elif request.method == 'GET':
        return "Método get para ANSWER!!!"