from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from nodes import responder, refinar, classificar_intencao
from custom_types import StateAtendimento

# Iniciando o grafo
graph_builder = StateGraph(StateAtendimento)

# Adicionando os nós
graph_builder.add_node("responder", responder)
graph_builder.add_node("node_refinar", refinar)
graph_builder.add_node("classificar_intencao", classificar_intencao)

# Personalizando as pontes/edges
graph_builder.add_edge(START, "node_refinar")
graph_builder.add_edge("node_refinar", "classificar_intencao")
graph_builder.add_conditional_edges("classificar_intencao", lambda state: next(iter(state['intention'])), {"1": "responder", "2": "responder", "3": "responder", "4": "responder", "5": "responder"})
graph_builder.add_edge("responder", END)

# Compilando o grafo
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)