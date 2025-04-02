from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from nodes import responder, refinar, classificar_intencao, coletar_dados, escrever_consulta
from custom_types import StateAtendimento

# Iniciando o grafo
graph_builder = StateGraph(StateAtendimento)

# Adicionando os nós
graph_builder.add_node("responder", responder)
graph_builder.add_node("node_refinar", refinar)
graph_builder.add_node("classificar_intencao", classificar_intencao)
graph_builder.add_node("coletar_dados", coletar_dados)
graph_builder.add_node("escrever_consulta", escrever_consulta)

# Personalizando as pontes/edges
graph_builder.add_edge(START, "node_refinar")
graph_builder.add_edge("node_refinar", "classificar_intencao")
graph_builder.add_conditional_edges(
    "classificar_intencao", 
    lambda state: next(iter(state['intention'])), 
    {
        "1": "coletar_dados", 
        "2": "responder", 
        "3": "responder", 
        "4": "responder", 
        "5": "responder"
    }
)
graph_builder.add_conditional_edges(
    "coletar_dados",
    lambda state: state["consultar"],
    {
        "true": "escrever_consulta",
        "false": END
    }
)
graph_builder.add_edge("responder", END)

# Compilando o grafo
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)