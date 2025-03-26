from vector_stores import vector_store_imoveis, vector_store_perguntas, vector_store_perfis
from langchain_core.tools import tool
from langgraph.prebuilt.tool_node import ToolNode
import sqlite3
from typing import Dict
from pydantic import BaseModel

@tool
def buscar_imoveis (query: str) -> str:
    """Buscar imóveis disponíveis para locação/aluguel"""
    docs = vector_store_imoveis.similarity_search(query)
    response = "\n\n".join([doc.page_content for doc in docs])
    return response

# @tool
# def ler_instrucoes (query: str) -> str:
#     """Instruções sobre processos administrativos da Imobiliária Stylus"""
#     docs = vector_store_instrucoes.similarity_search(query)
#     return "\n\n".join([doc.page_content for doc in docs])

@tool
def perguntas_frequentes (query: str) -> str:
    """Respostas a perguntas frequentes dos clientes"""
    docs = vector_store_perguntas.similarity_search(query)
    return "\n\n".join([doc.page_content for doc in docs])

db_path = "docs/perfis.sqlite3"


@tool
def gerenciar_perfil_cliente(novas_informacoes: Dict) -> str:
    """
    Adiciona ou atualiza um perfil no banco de dados SQLite.

    Args:
        novas_informacoes (Dict): Informações do perfil.

    Returns:
        str: Mensagem de sucesso ou erro.
    """
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar se o perfil já existe
        cursor.execute("SELECT 1 FROM perfis WHERE id = ?", (novas_informacoes.get("id"),))
        perfil_existente = cursor.fetchone()

        if perfil_existente:
            # Atualizar o perfil existente
            campos_atualizar = ", ".join(
                f"{campo} = ?" for campo in novas_informacoes if campo != "id"
            )
            valores = tuple(novas_informacoes[campo] for campo in novas_informacoes if campo != "id")
            valores += (novas_informacoes["id"],)

            consulta = f"UPDATE perfis SET {campos_atualizar} WHERE id = ?"
            cursor.execute(consulta, valores)
        else:
            # Inserir um novo perfil
            colunas = ", ".join(novas_informacoes.keys())
            placeholders = ", ".join("?" for _ in novas_informacoes)
            valores = tuple(novas_informacoes.values())

            consulta = f"INSERT INTO perfis ({colunas}) VALUES ({placeholders})"
            cursor.execute(consulta, valores)

        conn.commit()
        return "Perfil atualizado ou adicionado com sucesso."
    except sqlite3.Error as e:
        return f"Erro ao acessar o banco de dados: {e}"
    except KeyError as e:
        return f"Erro: Chave ausente nas informações fornecidas: {e}"
    finally:
        if conn:
            conn.close()

tools = [buscar_imoveis, perguntas_frequentes, gerenciar_perfil_cliente]
tools_node = ToolNode(tools)