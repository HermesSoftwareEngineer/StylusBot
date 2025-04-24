from tools import cadastrar_atendimento
from custom_types import StateCadastrarAtendimento, State

# def test_criar_atendimento_valid_data():
#     # Mock valid input data for creating an atendimento
#     input_data = StateCadastrarAtendimento(
#         ClienteNome="João Silva",
#         ClienteTelefone="123456789",
#         Midia="Instagram",
#     )

#     # Call the function and capture the result
#     result = cadastrar_atendimento(input_data)

#     return {"atendimentoCadastrado": True}

# print(test_criar_atendimento_valid_data())

state_test = State(
    messages=["Olá!"]
)

print("state_test", state_test)