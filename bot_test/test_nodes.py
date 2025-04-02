from nodes import escrever_consulta
from langchain_core.messages import AIMessage

# Mock state with necessary data for testing
state = {
    "refined": AIMessage(content="Quero consultar apartamentos para alugar em Fortaleza-CE."),
    "query": None
}

try:
    # Call the function and print the result
    response = escrever_consulta(state)
    print(response)
except ValueError as e:
    print(f"Erro: {e}")