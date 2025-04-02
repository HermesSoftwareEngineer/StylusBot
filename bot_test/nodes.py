from custom_types import StateAtendimento, prompt_template_responder, query_prompt_template
from langchain_core.messages import SystemMessage, AIMessage
from llm import llm
from typing_extensions import Annotated, TypedDict
from create_db import engine as db
from sqlalchemy import MetaData

class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]

def refinar(state: StateAtendimento):

    mensagem_usuario = state['messages'][-1].content
    system_message = (
        f"""
            Melhore a mensagem a seguir, deixando-a mais clara e objetiva, mas sem fazer perder a ideia original: '{mensagem_usuario.strip()}'
            Retorne: 'Mensagem melhorada: ...'
        """
    )

    llm_response = llm.invoke([system_message])
    return { **state, 'refined': llm_response }

def responder(state: StateAtendimento):

    query = state['messages'] + [SystemMessage(content=state['refined'].content)]
    prompt = prompt_template_responder.invoke(query)
    response_llm = llm.invoke(prompt)
    
    return { **state, 'messages': response_llm }

def classificar_intencao(state: StateAtendimento):
    
    intention_map = {
            "1": "Buscar um imóvel",
            "2": "Tirar dúvidas",
            "3": "Exigir suporte humano",
            "4": "Nenhuma das opções",
            "5": "Erro de classificação de intenção"
        }

    response = "5"
    responder = False

    while not responder:
        system_message = SystemMessage(content=
            f"""
                Analise as mensagens e determine a intenção do usuário:
                1 - Buscar um imóvel (informações, valores, etc)
                2 - Tirar dúvidas (aluguel, documentação, burocracia, etc)
                3 - Exigir suporte humano
                4 - Nenhuma das opções
                
                Retorne apenas com o número da intenção (1, 2, 3 ou 4). Obedeça a regra estritamente. O retorno precisa ser um número!
            """
        )

        query = state['messages'] + [SystemMessage(content=state['refined'].content)] + [system_message]

        response_llm = llm.invoke(query)
        response_llm = str(response_llm.content).strip()  # Remove espaços no início e no final
        response_llm = response_llm.replace(" ", "")  # Remove todos os espaços dentro da string
        response_llm = response_llm.replace("\n", "")  # Remove todos os espaços dentro da string
        print(f"CLASSIFICAÇÃO DE INTENÇÃO DO LLM: {response_llm}")

        if response_llm not in intention_map:
            query = f"Sua resposta foi um número? Você tem certeza que respondeu conforme as regras?\n\n Sua resposta: {response_llm}"
        else:
            response = response_llm
            responder = True
        
    print(f"Classificação final: {response}")
    return { **state, 'intention': {response: intention_map[response]}}

def coletar_dados(state: StateAtendimento):
    repetir = True
    response_message = "Sem erros por enquanto"

    while repetir:
        system_message = SystemMessage(content=
            """
            Para realizar uma consulta de imóveis no banco de dados, precisamos ter uma das combinações de informações:
            - Combinação 1: Tipo de imóvel, bairros procurados e valor máximo disposto a pagar
            - Combinação 2: Código do anúncio, apenas

            Verifique se temos uma das combinações com informações completas. Se não, solicite o que falta ao usuário.

            Retorne com este formato JSON:
            {
                "response": "Resposta que será exibida ao usuário",
                "consultar": true/false
            }
            """
        )

        # Adiciona a mensagem de resposta anterior ao prompt
        prompt = state['messages'] + [SystemMessage(content=state['refined'].content)] + [system_message] + [AIMessage(content=response_message)]
        llm_response = llm.invoke(prompt)

        try:
            # Parse the LLM response como JSON
            parsed_response = llm_response.json()
            response_message = parsed_response.get("response", "Erro ao processar a resposta.")
            consultar = "true" if parsed_response.get("consultar", False) else "false"
            repetir = False  # Sai do loop se o JSON for válido
        except (ValueError, AttributeError):
            # Trata respostas inválidas ou malformadas
            response_message = "Não foi possível interpretar a resposta. Por favor, reformule sua solicitação."
            consultar = "false"
            repetir = True  # Continua no loop para tentar novamente

    # Atualiza o estado com a resposta e a flag de consulta
    return {
        **state,
        "messages": [AIMessage(content=response_message)],
        "consultar": consultar
    }

def escrever_consulta(state: StateAtendimento):
    """Gera a consulta SQL para buscar informações"""
    metadata = MetaData()
    metadata.reflect(bind=db) 
    table_info = {table.name: [col.name for col in table.columns] for table in metadata.sorted_tables}

    prompt = query_prompt_template.invoke(
        {
            "dialect": db.dialect.name,
            "top_k": 10,
            "table_info": table_info,
            "input": state["refined"]
        }
    )

    llm_estruturado = llm.with_structured_output(QueryOutput)
    result = llm_estruturado.invoke(prompt)
    print(f"Resultado: {result['query']}")

    return { **state, "query": result["query"] }