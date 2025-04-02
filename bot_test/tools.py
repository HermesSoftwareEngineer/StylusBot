from langchain_core.tools import tool
from vector_stores import vector_store_imoveis

@tool
def buscar_imoveis (query: str) -> str:
    """Buscar imóveis disponíveis para locação/aluguel"""
    docs = vector_store_imoveis.similarity_search(query)
    response = "\n\n".join([doc.page_content for doc in docs])
    return response