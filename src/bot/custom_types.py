from typing_extensions import TypedDict, Annotated, List, Literal
from langgraph.graph.message import add_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field

class State(TypedDict):
    atendimentoCadastrado: bool = False
    messages: Annotated[list[str], add_messages]

class RespostaNodeCadastrarAtendimento(BaseModel):
    """Resposta do nó de cadastrar atendimento"""
    mensagem: str = Field(description="Mensagem ao usuário")
    statusCadastro: bool = Field(description="Status do cadastro do atendimento")

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

class StateCadastrarAtendimento(TypedDict):
    ClienteNome: str
    ClienteTelefone: str
    Midia: str

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

def validar_cadastro_atendimento(state: State):
    print("State:", state)
    return state["atendimentoCadastrado"]