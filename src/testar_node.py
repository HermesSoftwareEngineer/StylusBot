from nodes import atualizar_perfil, consultar_ou_responder

state = {
    'messages': [
        {
            'type': 'system',
            'content': "Você é um atendente da Imobiliária Stylus chamado 'StylusBot'. Responda da melhor maneira possível. Utilize as ferramentas sempre que precisar. Se não souber a resposta, basta dizer que não sabe."
        },
        {
            'type': 'human',
            'content': "Sou o Hermes. Gostaria de alugar um apartamento de 2 quartos em São Paulo."
        }
    ]
}

# ----------------------------------------------------------------------------
# TESTANDO O NÓ ATUALIZAR_PERFIL
# ----------------------------------------------------------------------------

# response = atualizar_perfil(state)
# print(response)

# ----------------------------------------------------------------------------
# TESTANDO O NÓ CONSULTAR_OU_RESPONDER
# ----------------------------------------------------------------------------

# response = consultar_ou_responder(state)
# print(response)