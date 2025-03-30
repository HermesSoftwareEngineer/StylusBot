from tools import gerenciar_perfil_cliente
from typing import Dict

# ----------------------------------------------------------------------------
# TESTANDO A FERRAMENTA GERENCIAR_PERFIL_CLIENTE

novas_informacoes = {
    "id": 2,
    "tipo_imovel": "Salas comerciais",
    "localizacao": "Fortaleza, Dionísio Torres",
    "valor_maximo": 2500,
    "quartos_banheiros": "1",
    "modalidade": "Aluguel",
    "observacao": "Próximo ao metrô",
    "nome": "Geordes Barbosa",
    "telefone": "11987654321"
}

# Chamando diretamente com um dicionário, pois LangChain converte automaticamente
resultado = gerenciar_perfil_cliente(dict(novas_informacoes))

print(resultado)
# ----------------------------------------------------------------------------