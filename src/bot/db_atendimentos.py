from sqlalchemy import create_engine

# Conectar ao banco
engine = create_engine("sqlite:///atendimentos.db")

sql_commands = [
    "DROP TABLE IF EXISTS atendimentos_temp;",
    """
    CREATE TABLE atendimentos_temp (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Codigo TEXT,
        Finalidade TEXT,
        ClienteNome TEXT,
        ClienteTelefone TEXT,
        ClienteEmail TEXT,
        Midia TEXT,
        Tipo TEXT,
        SituacaoDescarte TEXT,
        ImoveisCarrinho TEXT,
        PerfilQuartos INTEGER,
        PerfilBanhos INTEGER,
        PerfilSuites INTEGER,
        PerfilVagas INTEGER,
        PerfilValorDe REAL,
        PerfilValorAte REAL,
        PerfilAreaInternaDe REAL,
        PerfilAreaInternaAte REAL,
        PerfilTipos TEXT,
        PerfilCidades TEXT,
        PerfilBairros TEXT,
        PerfilRegioes TEXT,
        Valor REAL,
        PerfilSistema TEXT,
        Indicacao TEXT
    );
    """,
    """INSERT INTO atendimentos_temp (
        Codigo, Finalidade, ClienteNome, ClienteTelefone, ClienteEmail, Midia, Tipo, SituacaoDescarte,
        ImoveisCarrinho, PerfilQuartos, PerfilBanhos, PerfilSuites, PerfilVagas, PerfilValorDe, PerfilValorAte,
        PerfilAreaInternaDe, PerfilAreaInternaAte, PerfilTipos, PerfilCidades, PerfilBairros, PerfilRegioes,
        Valor, PerfilSistema, Indicacao
    ) 
    SELECT 
        Codigo, Finalidade, ClienteNome, ClienteTelefone, ClienteEmail, Midia, Tipo, SituacaoDescarte,
        ImoveisCarrinho, PerfilQuartos, PerfilBanhos, PerfilSuites, PerfilVagas, PerfilValorDe, PerfilValorAte,
        PerfilAreaInternaDe, PerfilAreaInternaAte, PerfilTipos, PerfilCidades, PerfilBairros, PerfilRegioes,
        Valor, PerfilSistema, Indicacao
    FROM atendimentos;""",
    "DROP TABLE atendimentos;",
    "ALTER TABLE atendimentos_temp RENAME TO atendimentos;"
]

# Executando cada comando individualmente
with engine.connect() as connection:
    for sql in sql_commands:
        connection.exec_driver_sql(sql)
