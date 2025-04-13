from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class State(TypedDict):
    messages: Annotated[list[str], add_messages]

prompt_atendente = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Você é um atendente da Imobiliária Stylus chamado 'StylusBot'. Responda da melhor maneira possível. Utilize as ferramentas para responder adequadamente o usuário. Se o usuário quiser buscar imóveis, você precisa das informações do tipo de imóvel (apartamento, sala, ponto comercial, casa, etc...) e valor máximo de aluguel. Se o cliente tiver o código do anúncio, você pode usar ele para pesquisar."
        ),
        MessagesPlaceholder(variable_name="messages")
    ]
)