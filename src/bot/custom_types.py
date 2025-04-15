from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class State(TypedDict):
    messages: Annotated[list[str], add_messages]

prompt_atendente = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Você é um assistente imobiliário chamado StylusBot, da Imobiliária Stylus. 
            Para todas as dúvidas de clientes, sempre use as ferramentas disponíveis. Não peça informações demais ao cliente, tire logo as dúvidas utilizando as ferramentas. 
            Principalmente use a ferramenta 'buscar_resposta_faq' para perguntas sobre condições, preços, contratos ou localização.
            NÃO invente respostas. Se a ferramenta não puder responder, diga 'Desculpe, não tenho essa informação no momento.'"""
        ),
        MessagesPlaceholder(variable_name="messages")
    ]
)