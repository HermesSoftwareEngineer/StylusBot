from langgraph.prebuilt.tool_node import ToolNode
from tools import tools
from custom_types import State, prompt_atendente, prompt_analista, ResultadoAnalise
from llms import llm
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage
from vector_stores import vector_store_prompts

tools_node = ToolNode(tools)

def analisar_mensagem(state: State):

    prompts = vector_store_prompts.similarity_search(state['messages'][-1].content, k=5)
    
    system_message = f"""
    Última mensagem do cliente: {state['messages'][-1].content}\n\n
    Últimas mensagens da conversa: {state['messages'][-40:]}\n\n
    Prompts disponíveis:\n
    {prompts}\n\n
    """
    prompt = prompt_analista.invoke(system_message)
    responder = llm.with_structured_output(ResultadoAnalise).invoke(prompt)
    print("RESPOSTA DO LLM: ", responder)
    return {**state, "prompt": responder["answer"]}

def consultar_ou_responder(state: State):
    prompt = prompt_atendente.invoke(state["messages"][-40:])
    response = llm.bind_tools(tools).invoke(prompt)
    # tools, tool_choice='any'
    # print("RESPOSTA DO LLM: ", response)
    return {"messages": response}

def responder(state: State):
    """Gerando respostas com base na ferramenta de consultar imóveis"""
    list_messages_tools = [m for m in reversed(state['messages']) if m.type == 'tool']
    docs_messages_tools = '\n\n'.join(m.content for m in reversed(list_messages_tools[-40:]))

    system_message = SystemMessage(
        'SE TIVER IMÓVEIS NO BANCO DE DADOS (result), responda com:'
        '* 📍 **Endereço:** [endereço do imóvel]\n'
        '* 🏡 **Descrição:** [descrição curta do imóvel]\n'
        '* 💰 **Valor:** [valor do aluguel + encargos]\n'
        '* 🔗 **Links de anúncio:** [se não tiver links, oculte essa parte]\n\n'
        'SE NÃO TIVER IMÓVEIS NO BANCO DE DADOS (result), apenas diga que não tem imóveis com as características, mas poderia tentar com outras características. Seja gentil.'
        '\n\n' + docs_messages_tools
    )

    conversation_messages = [
        m for m in state['messages']
        if m.type in ('system', 'human')
        or (m.type == 'ia' and not m.tool_calls)
    ]
    
    prompt = [system_message] + conversation_messages[-40:]

    return {'messages': llm.invoke(prompt)}