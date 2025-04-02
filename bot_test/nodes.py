from custom_types import StateAtendimento, prompt_template_responder
from langchain_core.messages import SystemMessage, AIMessage
from llm import llm

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
    system_message = SystemMessage(content=
        f"""
        Para realizar uma consulta de imóveis no banco de dados. Precisamos ter uma das combinações de informações:
        - Combinação 1: Tipo de imóvel, bairros procurados e valor máximo disposto a pagar
        - Combinação 2: Código do anúncio, apenas

        VERIFIQUE SE TEMOS UMA DAS COMBINAÇÕES COM INFORMAÇÕES COMPLETAS. SE NÃO, SOLICITE O QUE FALTA AO USUÁRIO. 
        """
    )

    prompt = state['messages'] + [SystemMessage(content=state['refined'].content)] + [system_message]
    response = llm.invoke(prompt)

    return { **state, "messages": response }