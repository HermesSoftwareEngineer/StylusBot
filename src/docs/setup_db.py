import sqlite3

db_path = "perfis.sqlite3"

# Conectar ao banco
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS perfis (
    id INTEGER PRIMARY KEY,
    tipo_imovel TEXT,
    localizacao TEXT,
    valor_maximo INTEGER,
    quartos_banheiros TEXT,
    modalidade TEXT,
    observacao TEXT,
    nome TEXT,
    telefone TEXT
);
""")

conn.commit()
conn.close()

print("Banco de dados e tabela configurados com sucesso.")
