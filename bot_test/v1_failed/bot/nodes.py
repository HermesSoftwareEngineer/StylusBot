from .vector_stores import llm 
from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState
from .tools import tools, gerenciar_perfil_cliente
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt_template = ChatPromptTemplate(
    [
        (
            "system",
            "Você é um atendente da Imobiliária Stylus chamado 'StylusBot'. Responda da melhor maneira possível. Utilize as ferramentas sempre que precisar. Se não souber a resposta, basta dizer que não sabe."
        ),
        (
            "system",
            "SEMPRE QUE O USUÁRIO PASSAR ALGUMA INFORMAÇÃO DO PERFIL DE IMÓVEL PROCURADO, UTILIZE A FERRAMENTE DE BUSCAR IMÓVEIS"
        ),
        MessagesPlaceholder(variable_name='messages')
    ]
)


def atualizar_perfil(state: MessagesState):
    """Atualiza o perfil do usuário, se necessário"""

    # Solicita ao LLM que gere um dicionário com as novas informações do perfil
    system_message = SystemMessage("""
    Gere um dicionário JSON com as seguintes informações para atualizar um perfil de usuário:
    - id (int): Identificador do usuário.
    - tipo_imovel (str): Tipo do imóvel, como 'casa' ou 'apartamento'.
    - localizacao (str): Bairro, cidade e estado.
    - valor_maximo (int): Valor máximo que o usuário deseja pagar.
    - quartos_banheiros (str): Exemplo: '2 quartos, 1 banheiro'.
    - modalidade (str): 'aluguel' ou 'compra'.
    - observacao (str): Observação adicional do usuário.
    - nome (str): Nome completo do usuário.
    - telefone (str): Número de telefone do usuário.

    Responda apenas com um JSON válido, sem explicações. Adicione conteúdo apenas nas informações que você tiver.
    """)

    prompt = [system_message] + state['messages']  # Adiciona a mensagem do sistema ao contexto

    response = llm.bind_tools([gerenciar_perfil_cliente], force=True).invoke(prompt)  # Chama o LLM para gerar os dados
    novas_informacoes = response.content  # Converte a resposta para um dicionário

    return {'messages': novas_informacoes}

# ----------------------------------------------------------------------------

def consultar_ou_responder(state: MessagesState):
    """Usa o LLM para decidir se ferramentas devem ser consultadas"""
    
    tool_description = {
        "buscar_imoveis": "Busca imóveis disponíveis para locação.",
        "perguntas_frequentes": "Responde a perguntas frequentes dos clientes.",
        "gerenciar_perfil_cliente": "Adiciona ou atualiza informações no perfil do cliente."
    }

    prompt = prompt_template.invoke(state['messages'])

    llm_with_tools = llm.bind_tools(
        tools=tools,
        tool_descriptions=tool_description
    )

    # Invoca o LLM para tomar a decisão
    llm_response = llm_with_tools.invoke(prompt)

    return {'messages': llm_response}

# ----------------------------------------------------------------------------

def preparar_consulta(state: MessagesState):
    """Preparar texto de consulta para ferramentas"""
    system_message = SystemMessage(
        """Leia bem a pergunta do usuário e o contexto e em base disso elabore uma query para buscar informações nos documentos.
        Utilize sempre palavras chaves e relacionadas à dúvida do usuário, garantindo assertividade na utilização das ferramentas."""
    )

    conversation_messages = [
        m for m in state['messages']
        if m.type in ('system', 'human')
        or (m.type == 'ia' and not m.tool_calls)
    ]

    prompt = [system_message] + conversation_messages
    llm_with_tools = llm.bind_tools(tools)

    return {'messages': llm_with_tools.invoke(prompt)}

def gerar_resposta(state: MessagesState):
    """Gerando respostas com base nas ferramentas"""
    list_messages_tools = [m for m in reversed(state['messages']) if m.type == 'tool']
    docs_messages_tools = '\n\n'.join(m.content for m in reversed(list_messages_tools))

    system_message = SystemMessage(
        'Você é um assistente imobiliário. Sempre formate as respostas de imóveis da seguinte maneira:\n\n'
        '**🏠 Informações do imóvel!**\n\n'
        '* 📍 **Endereço:** [endereço do imóvel]\n'
        '* 🏡 **Descrição:** [descrição curta do imóvel]\n'
        '* 💰 **Valor:** [valor do aluguel + encargos]\n'
        '* 🔗 **Links de anúncio:** [links disponíveis]\n\n'
        'Se não encontrar imóveis, apenas diga "No momento, não temos imóveis disponíveis com essas características.'
        'Seja didático, diga: Encontrei alguns imóveis similares ao que você procura, veja se lhe agrada...'
        'Seja sempre claro e gentil nas respostas, não seja secos ou rudes."'
        '\n\n' + docs_messages_tools
    )

    conversation_messages = [
        m for m in state['messages']
        if m.type in ('system', 'human')
        or (m.type == 'ia' and not m.tool_calls)
    ]
    
    prompt = [system_message] + conversation_messages

    return {'messages': llm.invoke(prompt)}
