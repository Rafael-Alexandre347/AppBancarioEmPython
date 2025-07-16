print("""
        ----------------------------------------------
        || Bem-Vindo(a) ao aplicativo do banco DIO! || 
        ----------------------------------------------\n""")

clientes = []

def criar_usuario(clientes):
    cpf = input("Informe o CPF (somente números): ")
    if filtrar_usuario(cpf):
        print("\n   Já existe um usuário com esse CPF.")
        return None
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento no formato 'dd/mm/aaaa': ")
    endereco = input("Informe o endereço no formato 'Logradouro - Nº - Bairro - Cidade - Estado': ")

    clientes.append({
        "nome" : nome, 
        "data_nascimento" : data_nascimento, 
        "cpf" : cpf, 
        "endereco" : endereco})
    
    print("Usuário criado com sucesso.")
    return clientes

def menu():
    while True:
        print("""
              Selecione uma operação a ser realizada: 
            1 - Depósito 
            2 - Saque 
            3 - Verificar Extrato
            4 - Criar Novo Usuário
            5 - Criar Nova Conta 
            6 - Listar Contas
            0 - Sair do Aplicativo""")
        acao = input("      Informe com um dos números mostrados acima: ")
        return acao

def saque(*, saldo, valor, extrato, limite, qtd_saques, limite_saques):
    if qtd_saques >= limite_saques:
        print("Valor diário de saques atingido.")
    elif valor > saldo:
        print("Valor indisponível.")
    elif valor > limite:
        print("Valor acima do limite informado.")
    elif valor == 0:
        print("Valor inválido. Tente novamente.")
    else:
        saldo -= valor
        extrato.append(f"||Saque:    -R${valor:.2f}||")
        print(f"Saque no valor R${valor:.2f} realizado com sucesso.")
        return saldo, qtd_saques + 1, extrato
    return saldo, qtd_saques, extrato

def deposito(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato.append(f"||Depósito: +R${valor:.2f}||")
        print(f"Depósito no valor R${valor:.2f} realizado com sucesso.")
    else:
        print("Valor de depósito inválido.")
    return saldo, extrato

def extrato(saldo, *, extrato):
    print("||================||EXTRATO||================||")
    if extrato:
        for operacoes in extrato:
            print(f"   {operacoes}")
    else:
        print("Não há nenhuma movimentação disponível")
    print(f"   ||Saldo atual: R${saldo:.2f}||")
    print("||===========================================||")

def filtrar_usuario(cpf):

    for cliente in clientes:
        if cliente["cpf"] == cpf:
            return cliente
    return None

def criar_conta(agencia, numero_conta, usuario):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf)

    if usuario:
        print("\n   Conta criada com sucesso.")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    print("Usuário não encontrado.")

def listar_contas(contas):
    for conta in contas:
        linha = f"""
        Agência: {conta['agencia']},
        Número da conta: {conta['numero_conta']},
        Titular: {conta['usuario']['nome']}
        """
        print(linha)


def main():
    saldoConta = 0.0
    quantidadeSaques = 0
    operacoes = []
    LIMITE_POR_SAQUE = 500
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    contas = []

    while True:
        acao = menu()
        
        if acao == "1":
            try:
                valorDeposito = float(input("Informe o valor a ser depositado: "))
                saldoConta, operacoes = deposito(saldoConta, valorDeposito, operacoes)
            except ValueError:
                print("Entrada inválida. Tente novamente.")
            input()
        
        elif acao == "2":
            try:
                print(f"Você tem direito a {LIMITE_SAQUES} saques diários, com o valor máximo de R${LIMITE_POR_SAQUE:.2f} por operação.")
                valorSaque = float(input("Informe o valor a ser sacado: "))
                saldoConta, quantidadeSaques, operacoes = saque(
                    saldo = saldoConta,
                    valor = valorSaque,
                    extrato = operacoes,
                    limite = LIMITE_POR_SAQUE,
                    qtd_saques = quantidadeSaques,
                    limite_saques = LIMITE_SAQUES
                )
            except ValueError:
                print("Entrada inválida. Tente novamente.")
            input()
        
        elif acao == "3":
                extrato(saldo = saldoConta, extrato = operacoes)
                input()

        elif acao == "4":
            criar_usuario(clientes)

        elif acao == "5":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, clientes)

            if conta:
                contas.append(conta)
        
        elif acao == "6":
            listar_contas(contas)

        elif acao == "0" :
            print("     Obrigado por usar o nosso aplicativo!")
            break

        else : 
            print("      Operação não identificada. Por favor, tente novamente.\n")
            input()

main()