from custom_types import StateAtendimento, prompt_template_responder
from langchain_core.messages import SystemMessage
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