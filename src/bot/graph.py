from custom_types import State, validar_cadastro_atendimento
from langgraph.graph import StateGraph, START, END
from nodes import consultar_ou_responder, tools_node, responder, cadastrar_atendimento, inicializar, tools_node_de_cadastro_de_atendimento
from langgraph.prebuilt.tool_node import tools_condition
from langgraph.checkpoint.memory import MemorySaver

graph_builder = StateGraph(State)

graph_builder.add_node("consultar_ou_responder", consultar_ou_responder)
graph_builder.add_node("tools", tools_node)
graph_builder.add_node("tools_de_cadastro_de_atendimento", tools_node_de_cadastro_de_atendimento)
graph_builder.add_node("responder", responder)
graph_builder.add_node("cadastrar_atendimento", cadastrar_atendimento)
graph_builder.add_node("inicializar", inicializar)

graph_builder.add_edge(START, "inicializar")
graph_builder.add_conditional_edges("inicializar", validar_cadastro_atendimento, {True: "consultar_ou_responder", False: "cadastrar_atendimento"})
graph_builder.add_conditional_edges("cadastrar_atendimento", tools_condition, {"tools": "tools_de_cadastro_de_atendimento", END: END})
graph_builder.add_conditional_edges("consultar_ou_responder", tools_condition, {"tools": "tools", END: END})
graph_builder.add_edge("tools_de_cadastro_de_atendimento", "cadastrar_atendimento")
graph_builder.add_edge("cadastrar_atendimento", END)
graph_builder.add_edge("tools", "responder")
graph_builder.add_edge("responder", END)
graph_builder.add_edge("consultar_ou_responder", END)

memory = MemorySaver()
app = graph_builder.compile(checkpointer=memory)