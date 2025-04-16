from typing_extensions import TypedDict, Annotated, Optional, List
from langgraph.graph.message import add_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class State(TypedDict):
    messages: Annotated[list[str], add_messages]
    atendimentoCadastrado: bool = False

class StateAtendimento(TypedDict):
    Codigo: Optional[str]
    Finalidade: Optional[str]
    ClienteNome: str
    ClienteTelefone: str
    ClienteEmail: Optional[str]
    Midia: Optional[str]
    Tipo: Optional[str]
    SituacaoDescarte: Optional[str]
    ImoveisCarrinho: Optional[List[str]]
    PerfilQuartos: Optional[int]
    PerfilBanhos: Optional[int]
    PerfilSuites: Optional[int]
    PerfilVagas: Optional[int]
    PerfilValorDe: Optional[float]
    PerfilValorAte: Optional[float]
    PerfilAreaInternaDe: Optional[float]
    PerfilAreaInternaAte: Optional[float]
    PerfilTipos: Optional[List[str]]
    PerfilCidades: Optional[List[str]]
    PerfilBairros: Optional[List[str]]
    PerfilRegioes: Optional[List[str]]
    Valor: Optional[float]
    PerfilSistema: Optional[str]
    Indicacao: Optional[str]

prompt_atendente = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Você é um assistente imobiliário chamado StylusBot, da Imobiliária Stylus. Cadastre e atualize constantemente o atendimento do cliente via as ferramentas.
            Para todas as dúvidas de clientes, sempre use as ferramentas disponíveis. Não peça informações demais ao cliente, tire logo as dúvidas utilizando as ferramentas. 
            Principalmente use a ferramenta 'buscar_resposta_faq' para perguntas sobre condições, preços, contratos ou localização.
            NÃO invente respostas. Se a ferramenta não puder responder, diga 'Desculpe, não tenho essa informação no momento.'"""
        ),
        MessagesPlaceholder(variable_name="messages")
    ]
)