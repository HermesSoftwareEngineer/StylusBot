from db_imoveis import engine as db_imoveis

def validar_query(query: str):
    """
    Valida se a query SQL é sintaticamente correta.
    """
    try:
        with db_imoveis.connect() as conn:
            conn.execute(query)
        return True
    except Exception as e:
        print(f"Erro na validação da query: {e}")
        return f"Erro na validação da query: {e}"