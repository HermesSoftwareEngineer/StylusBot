from langgraph.prebuilt.tool_node import ToolNode
from tools import tools, tools_de_cadastro_de_atendimento
from custom_types import State, prompt_atendente, RespostaNodeCadastrarAtendimento
from llms import llm
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage

tools_node = ToolNode(tools)
tools_node_de_cadastro_de_atendimento = ToolNode(tools_de_cadastro_de_atendimento)
# tool_node_cadastrar_atendimento = ToolNode([cadastrar_atendimento])

def inicializar(state: State):
    if "atendimentoCadastrado" in state:
        print("EXISTE ATENDIMENTO CADASTRADO! veja: ", state['atendimentoCadastrado'])
        return state
    else:
        return {**state, "atendimentoCadastrado": False}

def cadastrar_atendimento(state: State):
    print("STATUS DO ATENDIMENTO CADASTRADO: ", state["atendimentoCadastrado"])
    if state["atendimentoCadastrado"] == False:
        system_message = SystemMessage(
            "Você é o StylusBot, atendente virtual da Imobiliária Stylus. Sempre se apresente antes de tudo."
            "Antes de responder às dúvidas do cliente, solicite os seguintes dados de atendimento: nome, telefone e mídia de origem "
            "(a mídia corresponde ao canal pelo qual o cliente conheceu a imobiliária). "
            "Após coletar todas as informações, cadastre o atendimento. "
        )
    else:
        system_message = SystemMessage(
            """Você é o StylusBot, atendente virtual da Imobiliária Stylus. Sempre se apresente antes de tudo.
            Informe ao cliente que o atendimento foi cadastrado com sucesso e que agora ele pode fazer perguntas sobre imóveis para alugar."""
        )

    conversation_messages = state["messages"]

    prompt = [system_message] + conversation_messages

    response = llm.bind_tools(tools_de_cadastro_de_atendimento).invoke(prompt)

    return {**state, "messages": response}

def consultar_ou_responder(state: State):
    prompt = prompt_atendente.invoke(state["messages"])
    response = llm.bind_tools(tools).invoke(prompt)
    # print(f"Resposta de consulta ou responder: ", response)
    return {**state, "messages": response}

def responder(state: State):
    """Gerando respostas com base nas ferramentas"""
    list_messages_tools = [m for m in reversed(state['messages']) if m.type == 'tool']
    docs_messages_tools = '\n\n'.join(m.content for m in reversed(list_messages_tools))

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
    
    prompt = [system_message] + conversation_messages

    return {**state, 'messages': llm.invoke(prompt)}