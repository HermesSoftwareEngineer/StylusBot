from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from typing import Annotated
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage
from langchain import hub

# Personalizando o estado do atendimento/mensagens
class StateAtendimento(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    refined: str
    intention: dict[str, str]
    consultar: str
    query: str
    result: str

prompt_template_responder = ChatPromptTemplate.from_messages([
    (
        "system", 
        "Você é o StylusBot, um atendente especializado em imóveis. Sempre se apresente ao falar com o cliente"
        "Responda de forma objetiva e clara, utilizando no máximo 3 frases para cada resposta. "
        "Seu objetivo é esclarecer dúvidas do usuário com precisão. Seja sempre educado."
    ),
    MessagesPlaceholder(variable_name="messages")
])

query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")