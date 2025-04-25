from langgraph.graph import StateGraph, START, END
from nodes import consultar_ou_responder, tools_node, responder
from langgraph.prebuilt.tool_node import tools_condition
from langgraph.checkpoint.memory import MemorySaver
from custom_types import State

graph_builder = StateGraph(State)

graph_builder.add_node("consultar_ou_responder", consultar_ou_responder)
graph_builder.add_node("tools", tools_node)
graph_builder.add_node("responder", responder)

graph_builder.add_edge(START, "consultar_ou_responder")
graph_builder.add_conditional_edges("consultar_ou_responder", tools_condition, {"tools": "tools", END: END})
graph_builder.add_edge("tools", "responder")
graph_builder.add_edge("responder", END)

memory = MemorySaver()
app = graph_builder.compile(checkpointer=memory)