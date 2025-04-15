import pandas as pd 
from sqlalchemy import create_engine

engine = create_engine("sqlite:///atendimentos.db")
df = pd.read_excel(r"C:\Users\Asus\PROJETOS_DEV\StylusBot\src\bot\dados_atendimentos.xlsx")

df = df.drop(["UnidadeCodigo", "Unidade", "Campanha", "Fase", "Termometro", "Mql", "Corretor", "Equipe", "Situacao", "ImoveisVisita", "ImoveisProposta", "DataHoraInclusao", "UsuarioInclusao", "DataHoraUltimaInteracao", "UltimaInteracao", "UsuarioUltimaInteracao"], axis=1)

df.to_sql("imoveis", con=engine, if_exists="replace", index=False)
print(df.columns.tolist())