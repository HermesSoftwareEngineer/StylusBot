from langgraph.prebuilt.tool_node import ToolNode
from tools import tools
from custom_types import State, prompt_atendente, prompt_analista, ResultadoAnalise
from llms import llm
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage
from vector_stores import vector_store_prompts

tools_node = ToolNode(tools)

def analisar_mensagem(state: State):
    # Busca os prompts mais similares à última mensagem do cliente
    print("Última mensagem do cliente:", state['messages'][-1].content)
    prompts = vector_store_prompts.similarity_search(state['messages'][-1].content, k=5)
    
    # Caso nenhum prompt seja encontrado, define uma mensagem padrão
    if not prompts:
        prompts = ["0 - Nenhum prompt encontrado"]
    
    # Cria a mensagem do sistema com as informações relevantes
    
    ultima_mensagem = state['messages'][-1].content
    prompts = "\n\n".join(
        [f"Título: {conteudo['titulo']}\nContexto: {conteudo['contexto']}\nPrompt: {conteudo['prompt']}" 
        for prompt in prompts 
        for conteudo in prompt["conteudos"]]
    )
    conversation_messages = "\n".join([m.content for m in state['messages'][-10:]])
    print("Prompts encontrados:", prompts)

    # Prepara o input para o modelo de análise
    prompt_input = {
        "input": ultima_mensagem, 
        "prompts": prompts,
        "messages": conversation_messages
    }
    prompt_value = prompt_analista.invoke(prompt_input)
    prompt = prompt_value.to_string()
    
    # Gera a resposta estruturada com base no modelo
    try:
        resposta = llm.with_structured_output(ResultadoAnalise).invoke(prompt)
    except Exception as e:
        print("Erro ao invocar o LLM:", e)

    # Retorna o estado atualizado com a resposta gerada
    return {**state, "prompt": resposta.answer}

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