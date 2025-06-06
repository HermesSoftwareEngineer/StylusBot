from typing_extensions import TypedDict, Annotated, List, Literal
from langgraph.graph.message import add_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field

class State(TypedDict):
    messages: Annotated[list[str], add_messages]
    prompt: int

class StateAtendimento(TypedDict):
    Finalidade: str
    ClienteNome: str
    ClienteTelefone: str
    ClienteEmail: str
    Midia: str
    Status: Literal["Em atendimento", "Cliente desistiu", "Negócio finalizado", "Outro"]
    PerfilQuartos: int
    PerfilBanheiros: int
    PerfilSuites: int
    PerfilVagas: int
    PerfilValorDe: float
    PerfilValorAte: float
    PerfilAreaInternaDe: float    
    PerfilAreaInternaAte: float
    PerfilTipos: List[str]
    PerfilCidades: List[str]
    PerfilBairros: List[str]
    PerfilRegioes: List[str]

class ResultadoAnalise(BaseModel):
    """
    Modelo utilizado para selecionar o prompt mais adequado para o LLM.
    """
    answer: int = Field(
        description="Número correspondente ao prompt ideal para o LLM, baseado na análise do contexto."
    )

prompt_atendente = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Sempre inicie a conversa se apresentando. Utilize emojis. Você é um assistente imobiliário chamado StylusBot, da Imobiliária Stylus. 
            Ferramentas disponíveis:
            - Consultar imóveis: Use esta ferramenta para consultar imóveis disponíveis com base nos critérios fornecidos pelo usuário.
            - Consultar perguntas frequentes: Use esta ferramenta sempre que o cliente fizer uma pergunta que pode estar no banco de Perguntas Frequentes (FAQ).
            Principalmente use a ferramenta 'buscar_resposta_faq' para perguntas sobre condições, preços, contratos ou localização.
            NÃO invente respostas. Se a ferramenta não puder responder, diga 'Desculpe, não tenho essa informação no momento. Entre em contato com: 85996688778 para mais informaç'"""
        ),
        MessagesPlaceholder(variable_name="messages")
    ]
)

prompt_analista = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Você é StylusBot, um assistente imobiliário da Imobiliária Stylus.
            Sua tarefa é analisar a mensagem do cliente e determinar o contexto mais adequado para gerar uma resposta precisa e útil.
            Considere as ferramentas disponíveis e as informações fornecidas pelo cliente.
            Retorne apenas a numeração do prompt escolhido, sem adicionar explicações ou comentários.

            Última mensagem do cliente: {input}\n\n
            Últimas mensagens da conversa: {messages}\n\n
            Prompts disponíveis:\n{prompts}\n\n
            """
        )
    ]
)