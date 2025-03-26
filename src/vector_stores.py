from dotenv import load_dotenv
from langchain_google_vertexai import ChatVertexAI, VertexAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import TextLoader, UnstructuredExcelLoader
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt.tool_node import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

# Carregando as variáveis de ambiente
load_dotenv()

# Iniciando o LLM
llm = ChatVertexAI(model_name='gemini-1.5-flash')

# Iniciando os embeddings
embeddings = VertexAIEmbeddings('textembedding-gecko-multilingual@001')
vector_store_perfis = InMemoryVectorStore(embeddings)
vector_store_imoveis = InMemoryVectorStore(embeddings)
vector_store_perguntas = InMemoryVectorStore(embeddings)

# Carregando os documentos
loader_perfis = TextLoader(r'C:\Users\Asus\PROJETOS_DEV\StylusBot\src\docs\perfis.txt', encoding="utf-8")
docs_perfis = loader_perfis.load()

loader_imoveis = UnstructuredExcelLoader(r'C:\Users\Asus\PROJETOS_DEV\RagLabs\ex03_atendente_imobiliario2\dados_imoveis.xlsx', encoding="utf-8")
docs_imoveis = loader_imoveis.load()

loader_perguntas = TextLoader(r'C:\Users\Asus\PROJETOS_DEV\StylusBot\src\docs\perguntas_frequentes.txt', encoding="utf-8")
docs_perguntas = loader_perguntas.load()

# Dividindo os documentos
text_splitter1 = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=150)
text_splitter2 = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)

split_imoveis = text_splitter2.split_documents(docs_imoveis)
split_perguntas_frequentes = text_splitter1.split_documents(docs_perguntas)
split_perfis = text_splitter1.split_documents(docs_perfis)

# Adiciona os documentos aos vector_stores
vector_store_imoveis.add_documents(split_imoveis)
vector_store_perfis.add_documents(split_perfis)
vector_store_perguntas.add_documents(split_perguntas_frequentes)
