from langgraph.prebuilt.tool_node import ToolNode
from tools import tools
from custom_types import State, prompt_atendente
from llms import llm
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage

tools_node = ToolNode(tools)

def consultar_ou_responder(state: State):
    prompt = prompt_atendente.invoke(state["messages"])
    response = llm.bind_tools(tools).invoke(prompt)
    # print(f"Resposta de consulta ou responder: ", response)
    return {"messages": response}

def responder(state: State):
    """Gerando respostas com base nas ferramentas"""
    list_messages_tools = [m for m in reversed(state['messages']) if m.type == 'tool']
    docs_messages_tools = '\n\n'.join(m.content for m in reversed(list_messages_tools))

    system_message = SystemMessage(
        'Você é um assistente imobiliário. Formate as respostas de imóveis de maneira similar a indicada abaixo:\n\n'
        '\n\n'
        '(TENHA SEMPRE UMA INTRODUÇÃO GENTIL): Olha, procurei aqui no meu banco de dados e encontrei algumas opções similares ao que você procura...'
        '* 📍 **Endereço:** [endereço do imóvel]\n'
        '* 🏡 **Descrição:** [descrição curta do imóvel]\n'
        '* 💰 **Valor:** [valor do aluguel + encargos]\n'
        '* 🔗 **Links de anúncio:** [se não tiver links, oculte essa parte]\n\n'
        'Se não encontrar imóveis, apenas diga "No momento, não temos imóveis disponíveis com essas características."'
        '\n\n' + docs_messages_tools
    )

    conversation_messages = [
        m for m in state['messages']
        if m.type in ('system', 'human')
        or (m.type == 'ia' and not m.tool_calls)
    ]
    
    prompt = [system_message] + conversation_messages

    return {'messages': llm.invoke(prompt)}