from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt.tool_node import tools_condition
from langgraph.checkpoint.memory import MemorySaver
from nodes import consultar_ou_responder, gerar_resposta, atualizar_perfil
from tools import tools_node


# ----------------------------------------------------------------------------
# PREPARANDO O FLUXO
# ----------------------------------------------------------------------------

# Inicializa o grafo de estados com o estado inicial MessagesState
graph_builder = StateGraph(MessagesState)

# Adiciona os nós ao grafo
graph_builder.add_node("consultar_ou_responder", consultar_ou_responder)  # Decide se consulta ferramentas ou responde diretamente
graph_builder.add_node("tools", tools_node)  # Nó para executar ferramentas
graph_builder.add_node("gerar_resposta", gerar_resposta)  # Gera uma resposta final
graph_builder.add_node("atualizar_perfil", atualizar_perfil)  # Atualiza o perfil do cliente

# Define as transições entre os nós
graph_builder.add_edge(START, "atualizar_perfil")  # O fluxo começa atualizando o perfil
graph_builder.add_conditional_edges(
    "atualizar_perfil", 
    tools_condition,  # Condição para decidir se ferramentas são necessárias
    {"tools": "tools", END: "consultar_ou_responder"}  # Vai para "tools" ou "consultar_ou_responder"
)
graph_builder.add_edge("atualizar_perfil", "consultar_ou_responder")  # Caminho direto para "consultar_ou_responder"
graph_builder.add_conditional_edges(
    "consultar_ou_responder", 
    tools_condition,  # Condição para decidir se ferramentas são necessárias
    {"tools": "tools", END: END}  # Vai para "tools" ou encerra o fluxo
)
graph_builder.add_edge("tools", "gerar_resposta")  # Após usar ferramentas, gera uma resposta
graph_builder.add_edge("gerar_resposta", END)  # Finaliza o fluxo após gerar a resposta

# Configura o sistema de checkpoint para salvar o estado
memory = MemorySaver()

# Compila o grafo com o sistema de checkpoint
graph = graph_builder.compile(checkpointer=memory)