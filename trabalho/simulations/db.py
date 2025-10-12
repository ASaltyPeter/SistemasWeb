banco_fake = []

def salvar_no_banco(dado):
    banco_fake.append(dado)
    print(f"Dado salvo no banco: {dado}")

def listar_dados():
    return banco_fake
