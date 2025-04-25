from langchain_core.tools import tool
from llms import llm
from langchain_core.prompts import ChatPromptTemplate
from langchain import hub
from db_imoveis import engine as db_imoveis
from sqlalchemy import MetaData
from typing_extensions import Annotated, TypedDict
import pandas as pd
from vector_stores import vector_store_FAQ
from db_atendimentos import engine as db_atendimentos
from utils import validar_query

class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]

query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

@tool
def consultar_imoveis(input: str):
    """Use esta ferramenta para buscar imóveis disponíveis com base nos critérios informados pelo usuário. A cidade é sempre Fortaleza.
    Para realizar a busca, é necessário fornecer pelo menos uma das seguintes combinações de dados:
    - Tipo do imóvel (ex: apartamento, casa)
    - Código do imóvel ou do anúncio
    - Endereço, rua ou avenida
    - Outros dados relevantes que possam ajudar na busca
    
    No input, seja específico e sempre dê uma ordem de CONSULTA para o assistente buscar os imóveis."""

    consultar = True
    quantidade = 0

    input_customize = input + "\n\nSEMPRE RETORNE OS VALORES DO IMÓVEL (ALUGUEL, CONDOMÍNIO, ENCARGOS, ETC...) além do endereço, bairro, área, quantidade de quartos, quantidade de banheiros e código. A situação deve ser sempre 'Vago/Disponível'. NÃO INCLUA FINALIDADE NA CONSULTA, NÃO INCLUA."

    while consultar & (quantidade < 3):
    
        metadata = MetaData()
        metadata.reflect(bind=db_imoveis) 
        table_info = {table.name: [col.name for col in table.columns] for table in metadata.sorted_tables}
        
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

        if validar_query(query["query"]) != True:
            quantidade += 1
            input_customize = input + "\n\nA CONSULTA ANTERIOR NÃO FOI BEM-SUCEDIDA! Por favor, gere uma consulta SQL válida e SEMPRE inclua os seguintes detalhes sobre o imóvel: VALORES (ALUGUEL, CONDOMÍNIO, ENCARGOS, ETC.), endereço, bairro, área, quantidade de quartos, quantidade de banheiros e código. Certifique-se de que a situação do imóvel seja 'Vago/Disponível'. NÃO INCLUA FINALIDADE NA CONSULTA. Seja claro, preciso e garanta que a consulta seja sintaticamente correta."
        else:
            consultar = False

    df_filtrado = pd.read_sql(query["query"], con=db_imoveis)

    result = df_filtrado.to_string()
    # print(f"Resultado DA QUERY: {result}")
    
    if df_filtrado.empty:
        return {"result": "Nenhum imóvel encontrado para os critérios fornecidos. Informe ao usuário que não tem imóveis para esses critérios, que você pode tentar com critérios diferentes."}

    result = df_filtrado.to_string()
    # print(f"Resultado: {result}")

    return {"result": result}

@tool
def consultar_perguntas_frequentes(input: str):
    """Use esta ferramenta sempre que o cliente fizer uma pergunta que pode estar no banco de Perguntas Frequentes (FAQ). Perguntas sobre:
    - Visitas, chaves, agendamentos, horários, etc.
    - Como alugar, como funciona, etc.
    - Contratos, documentos, etc.
    - Documentação, como funciona, etc.
    - Formas de garantia, caução, fiador, seguro fiança, etc.
    - Boleto, vencimento, etc.
    - Burocracia, documentação, ficha cadastral, comprovante de renda, etc.
    - Entre outros semelhantes
    """
    result = vector_store_FAQ.similarity_search(input)
    return {"result": result}

tools = [consultar_imoveis, consultar_perguntas_frequentes]