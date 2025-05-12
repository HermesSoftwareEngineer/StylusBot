from langgraph.graph import StateGraph, START, END
from nodes import analisar_mensagem, tools_node, responder
from langgraph.prebuilt.tool_node import tools_condition
from langgraph.checkpoint.memory import MemorySaver
from custom_types import State

graph_builder = StateGraph(State)

graph_builder.add_node("analisar_mensagem", analisar_mensagem)
graph_builder.add_node("tools", tools_node)
graph_builder.add_node("responder", responder)

graph_builder.add_edge(START, "analisar_mensagem")
graph_builder.add_edge("analisar_mensagem", END)

memory = MemorySaver()
app = graph_builder.compile(checkpointer=memory)