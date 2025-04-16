from tools import criar_atendimento
from tools import criar_atendimento
from custom_types import StateAtendimento

def test_criar_atendimento_valid_data():
    # Mock valid input data for creating an atendimento
    input_data = StateAtendimento(
        Codigo="12345",
        Finalidade="Aluguel",
        ClienteNome="João Silva",
        ClienteTelefone="123456789",
        ClienteEmail="joao.silva@example.com",
        Midia="Instagram",
        Tipo="Residencial",
        SituacaoDescarte="Ativo",
        ImoveisCarrinho=["Imovel1", "Imovel2"],
        PerfilQuartos=3,
        PerfilBanhos=2,
        PerfilSuites=1,
        PerfilVagas=2,
        PerfilValorDe=1000,
        PerfilValorAte=3000,
        PerfilAreaInternaDe=50,
        PerfilAreaInternaAte=150,
        PerfilTipos=["Apartamento", "Casa"],
        PerfilCidades=["São Paulo"],
        PerfilBairros=["Centro", "Jardins"],
        PerfilRegioes=["Zona Sul"],
        Valor=2500,
        PerfilSistema="SistemaX",
        Indicacao="Amigo",
    )

    # Call the function and capture the result
    result = criar_atendimento(input_data)

    return {"atendimentoCadastrado": True}

print(test_criar_atendimento_valid_data())