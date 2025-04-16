from langchain_google_vertexai import VertexAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import TextLoader, UnstructuredExcelLoader
from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Iniciando os embeddings
embeddings = VertexAIEmbeddings('textembedding-gecko-multilingual@001')
vector_store_FAQ = InMemoryVectorStore(embeddings)

# Carregando os documentos
# loader_FAQ = TextLoader(r'C:\Users\hermes.barbosa\PROJETOS_DEV\StylusBot\src\bot\FAQ.txt', encoding="utf-8")
loader_FAQ = TextLoader(r'C:\Users\Hermes\PROJETOS_DEV\StylusBot\src\bot\FAQ.txt', encoding="utf-8")
docs_FAQ = loader_FAQ.load()

# Dividindo os documentos
text_splitter1 = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=150)

split_FAQ = text_splitter1.split_documents(docs_FAQ)

# Adiciona os documentos aos vector_stores
vector_store_FAQ.add_documents(split_FAQ)