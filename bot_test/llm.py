import dotenv
from langchain_google_vertexai import ChatVertexAI
    
# Carrega as variáveis de ambiente do arquivo .env
dotenv.load_dotenv()

# Inicia o llm
llm = ChatVertexAI(model_name="gemini-1.5-flash")