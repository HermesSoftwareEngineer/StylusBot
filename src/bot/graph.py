from custom_types import State, validar_cadastro_atendimento
from langgraph.graph import StateGraph, START, END
from nodes import consultar_ou_responder, tools_node, responder, cadastrar_atendimento, tool_node_cadastrar_atendimento
from langgraph.prebuilt.tool_node import tools_condition
from langgraph.checkpoint.memory import MemorySaver

graph_builder = StateGraph(State)

graph_builder.add_node("consultar_ou_responder", consultar_ou_responder)
graph_builder.add_node("tools", tools_node)
graph_builder.add_node("responder", responder)
graph_builder.add_node("cadastrar_atendimento", cadastrar_atendimento)
graph_builder.add_node("tool_node_cadastrar_atendimento ", tool_node_cadastrar_atendimento)

graph_builder.add_conditional_edges(START, validar_cadastro_atendimento, {True: "consultar_ou_responder", False: "cadastrar_atendimento"})
graph_builder.add_conditional_edges("cadastrar_atendimento", tools_condition, {"tools": "tool_node_cadastrar_atendimento ", END: END})
graph_builder.add_conditional_edges("tool_node_cadastrar_atendimento ", lambda response: response, {True: "consultar_ou_responder", False: END})
graph_builder.add_conditional_edges("consultar_ou_responder", tools_condition, {"tools": "tools", END: END})
graph_builder.add_edge("tools", "responder")
graph_builder.add_edge("responder", END)
graph_builder.add_edge("consultar_ou_responder", END)

memory = MemorySaver()
app = graph_builder.compile(checkpointer=memory)