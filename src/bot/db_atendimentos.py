from sqlalchemy import create_engine

engine = create_engine("sqlite:///atendimentos.db")

sql_commands = [
    # """
    # -- Exclui a tabela atendimentos se já existir
    # DROP TABLE IF EXISTS atendimentos;
    # """,
    """
    CREATE TABLE IF NOT EXISTS atendimentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Finalidade TEXT,
        ClienteNome TEXT,
        ClienteTelefone TEXT,
        ClienteEmail TEXT,
        Midia TEXT,
        Status TEXT,
        PerfilQuartos INTEGER,
        PerfilBanheiros INTEGER,
        PerfilSuites INTEGER,
        PerfilVagas INTEGER,
        PerfilValorDe REAL,
        PerfilValorAte REAL,
        PerfilAreaInternaDe REAL,
        PerfilAreaInternaAte REAL,
        PerfilTipos TEXT,
        PerfilCidades TEXT,
        PerfilBairros TEXT,
        PerfilRegioes TEXT
    );
    """,
    # """
    # -- Verifica se a tabela atendimentos existe antes de tentar o INSERT
    # INSERT INTO atendimentos (
    #     Codigo, Finalidade, ClienteNome, ClienteTelefone, ClienteEmail, Midia, Tipo, SituacaoDescarte,
    #     ImoveisCarrinho, PerfilQuartos, PerfilBanhos, PerfilSuites, PerfilVagas, PerfilValorDe, PerfilValorAte,
    #     PerfilAreaInternaDe, PerfilAreaInternaAte, PerfilTipos, PerfilCidades, PerfilBairros, PerfilRegioes,
    #     Valor, PerfilSistema, Indicacao
    # ) 
    # SELECT 
    #     Codigo, Finalidade, ClienteNome, ClienteTelefone, ClienteEmail, Midia, Tipo, SituacaoDescarte,
    #     ImoveisCarrinho, PerfilQuartos, PerfilBanhos, PerfilSuites, PerfilVagas, PerfilValorDe, PerfilValorAte,
    #     PerfilAreaInternaDe, PerfilAreaInternaAte, PerfilTipos, PerfilCidades, PerfilBairros, PerfilRegioes,
    #     Valor, PerfilSistema, Indicacao
    # FROM atendimentos
    # WHERE EXISTS (SELECT 1 FROM sqlite_master WHERE type='table' AND name='atendimentos');
    # """,
]


with engine.connect() as connection:
    for sql in sql_commands:
        try:
            connection.exec_driver_sql(sql)
            # print(f"Comando executado: {sql}")
        except Exception as e:
            print(f"Erro executando: {sql} \n{e}")
