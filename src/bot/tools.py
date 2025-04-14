from langchain_core.tools import tool
from llms import llm
from langchain_core.prompts import ChatPromptTemplate
from langchain import hub
from create_db import engine as db
from sqlalchemy import MetaData
from typing_extensions import Annotated, TypedDict
import pandas as pd
from vector_stores import vector_store_FAQ

class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]

query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

@tool
def consultar_imoveis(input: str):
    """Use esta ferramenta para consultar imóveis disponíveis com base nos critérios fornecidos pelo usuário."""
    metadata = MetaData()
    metadata.reflect(bind=db) 
    table_info = {table.name: [col.name for col in table.columns] for table in metadata.sorted_tables}
    
    input_customize = input + "\n\nSEMPRE RETORNE OS VALORES DO IMÓVEL (ALUGUEL, CONDOMÍNIO, ENCARGOS, ETC...) além do endereço, bairro, área, quantidade de quartos, quantidade de banheiros e código. A situação deve ser sempre 'Vago/Disponível'"
    prompt = query_prompt_template.invoke(
        {
            "dialect": db.engine.name,
            "top_k": 5,
            "table_info": table_info,
            "input": input_customize
        }
    )

    query = llm.with_structured_output(QueryOutput).invoke(prompt)
    # print(f"query gerada: {query['query']}")

    df_filtrado = pd.read_sql(query["query"], con=db)
    
    if df_filtrado.empty:
        return {"result": "Nenhum imóvel encontrado para os critérios fornecidos. Informe ao usuário que não tem imóveis para esses critérios, que você pode tentar com critérios diferentes."}

    result = df_filtrado.to_string()
    # print(f"Resultado: {result}")

    return {"result": result}

@tool
def consultar_perguntas_frequentes(input: str):
    """Use essa ferramenta para saber o que responder ao usuário perguntas frequentes de maneira assertiva
        As perguntas podem ser sobre: Como alugar, documentação, caução, cauções, formas de garantia, visitas, agendamento de visitas, ficha cadastral, etc...
    """
    result = vector_store_FAQ.similarity_search(input)
    return {"result": result}

tools = [consultar_imoveis, consultar_perguntas_frequentes]