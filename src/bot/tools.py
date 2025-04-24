from langchain_core.tools import tool
from llms import llm
from langchain_core.prompts import ChatPromptTemplate
from langchain import hub
from db_imoveis import engine as db_imoveis
from sqlalchemy import MetaData
from typing_extensions import Annotated, TypedDict
import pandas as pd
from vector_stores import vector_store_FAQ
from custom_types import StateCadastrarAtendimento
from db_atendimentos import engine as db_atendimentos

class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]

query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

@tool
def consultar_imoveis(input: str):
    """Use esta ferramenta para consultar imóveis disponíveis com base nos critérios fornecidos pelo usuário."""
    metadata = MetaData()
    metadata.reflect(bind=db_imoveis) 
    table_info = {table.name: [col.name for col in table.columns] for table in metadata.sorted_tables}
    
    input_customize = input + "\n\nSEMPRE RETORNE OS VALORES DO IMÓVEL (ALUGUEL, CONDOMÍNIO, ENCARGOS, ETC...) além do endereço, bairro, área, quantidade de quartos, quantidade de banheiros e código. A situação deve ser sempre 'Vago/Disponível'"
    prompt = query_prompt_template.invoke(
        {
            "dialect": db_imoveis.engine.name,
            "top_k": 5,
            "table_info": table_info,
            "input": input_customize
        }
    )

    query = llm.with_structured_output(QueryOutput).invoke(prompt)
    # print(f"query gerada: {query['query']}")

    df_filtrado = pd.read_sql(query["query"], con=db_imoveis)
    
    if df_filtrado.empty:
        return {"result": "Nenhum imóvel encontrado para os critérios fornecidos. Informe ao usuário que não tem imóveis para esses critérios, que você pode tentar com critérios diferentes."}

    result = df_filtrado.to_string()
    # print(f"Resultado: {result}")

    return {"result": result}

@tool
def consultar_perguntas_frequentes(input: str):
    """Use esta ferramenta sempre que o cliente fizer uma pergunta que pode estar no banco de Perguntas Frequentes (FAQ). 
        NÃO tente responder sozinho. Primeiro consulte aqui.
    """
    result = vector_store_FAQ.similarity_search(input)
    return {"result": result}

# @tool
# def atualizar_atendimento(input: StateAtendimento):
#     """Sempre que novas informações sobre o perfil do cliente, do atendimento ou sobre o cliente chegarem, atualize o atendimento utilizando essa ferramenta"""
#     metadata = MetaData()
#     metadata.reflect(bind=db_atendimentos) 
#     table_info = {table.name: [col.name for col in table.columns] for table in metadata.sorted_tables}
    
#     input_customize = input + "\n\nFaça uma consulta SQL que atualiza o atendimento do cliente com base em novas informações adquiridas."
#     prompt = query_prompt_template.invoke(
#         {
#             "dialect": db_atendimentos.engine.name,
#             "top_k": 5,
#             "table_info": table_info,
#             "input": input_customize
#         }
#     )

#     query = llm.with_structured_output(QueryOutput).invoke(prompt)
#     # print(f"query gerada: {query['query']}")

#     df_filtrado = pd.read_sql(query["query"], con=db_atendimentos)
    
#     if df_filtrado.empty:
#         return {
#             "result": "Nenhum atendimento encontrado para os critérios fornecidos. Informe ao usuário que não há atendimentos com esses dados e que é possível tentar outros critérios."
#         }

#     result = df_filtrado.to_string()
#     # print(f"Resultado: {result}")

#     return {"result": result}
    
@tool
def cadastrar_atendimento(input: StateCadastrarAtendimento):
    """Criar um atendimento e cadastrá-lo diretamente no banco de dados."""
    metadata = MetaData()
    metadata.reflect(bind=db_atendimentos)
    atendimentos_table = metadata.tables.get("atendimentos")  # Substitua "atendimentos" pelo nome real da tabela

    if atendimentos_table is None:
        raise ValueError("Tabela 'atendimentos' não encontrada no banco de dados.")

    # Construa o dicionário com os dados do atendimento
    atendimento_data = {
        "ClienteNome": input["ClienteNome"],
        "ClienteTelefone": input["ClienteTelefone"],
        "Midia": input["Midia"],
    }

    # Insere os dados no banco de dados
    with db_atendimentos.connect() as connection:
        insert_stmt = atendimentos_table.insert().values(atendimento_data)
        connection.execute(insert_stmt)
        connection.commit()

    return {"atendimentoCadastrado": True}

tools = [consultar_imoveis, consultar_perguntas_frequentes, cadastrar_atendimento]