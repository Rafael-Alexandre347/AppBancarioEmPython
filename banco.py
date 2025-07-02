print("""
        ----------------------------------------------
        || Bem-Vindo(a) ao aplicativo do banco DIO! || 
        ----------------------------------------------\n""")
saldoConta = 0.0
quantidadeSaques = 0
operacaoRealizada = ""

while True:
    print("""
          Selecione uma operação a ser realizada: 
          1 - Depósito 
          2 - Saque 
          3 - Verificar Extrato 
          0 - Sair do Aplicativo""")
    acao = input("      Informe com um dos números mostrados acima: ")

    if acao == "1":
        valorDeposito = float(input("Informe o valor a ser depositado: "))
        saldoConta += valorDeposito
        print(f"Depósito no valor {valorDeposito} realizado com sucesso!\n")
        input()
        operacaoRealizada += f"     Depósito no valor {valorDeposito}\n"
    
    elif acao == "2":
        print("Você tem direito a 3 saques diários, com o valor máximo de R$500,00 por operação.")
        quantidadeSaques += 1
        if quantidadeSaques < 4: 
            valorSaque = float(input("Informe o valor a ser sacado: "))
            if valorSaque <= saldoConta and valorSaque <= 500 :
                saldoConta -= valorSaque
                print(f"Saque no valor {valorSaque} realizado com sucesso!\n")
                input()
                operacaoRealizada += f"     Saque no valor {valorSaque}\n"
            else:
                print("Saque não permitido. Verifique se você possui saldo disponível, ou se a operação não viola nenhuma de nossas diretrizes.\n")
                input()
        else:
            print("Saque não permitido, você já atingiu o limite diário de saques.\n")
            input()
    elif acao == "3":
            if operacaoRealizada != "":
                print("\n")
                print(operacaoRealizada)
            else:
                print("     Não foram realizadas movimentações.")    
            print(f"     Saldo: R${saldoConta:.2f}")
            input()
    elif acao == "0" :
        print("     Obrigado por usar o nosso aplicativo!")
        break
    else : 
        print("      Operação não identificada. Por favor, tente novamente.\n")
        input()