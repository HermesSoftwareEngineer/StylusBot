import pandas as pd
from sqlalchemy import create_engine

df = pd.read_excel(r"C:\Users\hermes.barbosa\PROJETOS_DEV\StylusBot\src\bot\dados_imoveis.xlsx")
# df = pd.read_excel(r"C:\Users\Asus\PROJETOS_DEV\StylusBot\src\bot\dados_imoveis.xlsx")

engine = create_engine("sqlite:///meu_banco.db")

df.to_sql("imoveis", con=engine, if_exists="replace", index=False)

# df_lido = pd.read_sql("SELECT * FROM imoveis", con=engine)
# print(df_lido.head()) 