from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from nodes import responder, refinar
from custom_types import StateAtendimento

# Iniciando o grafo
graph_builder = StateGraph(StateAtendimento)

# Adicionando os nós
graph_builder.add_node("responder", responder)
graph_builder.add_node("node_refinar", refinar)

# Personalizando as pontes/edges
graph_builder.add_edge(START, "node_refinar")
graph_builder.add_edge("node_refinar", "responder")
graph_builder.add_edge("responder", END)

# Compilando o grafo
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)