from abc import ABC, abstractmethod
from datetime import datetime 

def log_transacao(func):
    def wrapper(*args, **kwargs):
        print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Executando: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

#============================================Classes=======================================================#

class Cliente:
    def __init__ (self, endereco):       
        self.endereco = endereco
        self.contas = []

    def realizar_transacoes (self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta (self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__ (self, endereco, cpf, nome, data_nascimento):
        super().__init__ (endereco)

        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
    def __init__ (self, saldo, numero, agencia, cliente, historico):

        self.saldo = saldo
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = historico

    def saldo(self):
        return self.saldo
        
    def sacar(self, valor):
        if valor > self.saldo:
            print ("Valor indisponível")
            return False
            
        self.saldo -= valor
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("Valor inválido. Tente novamente.")
            return False
            
        self.saldo += valor
        return True
        
    @classmethod
    def nova_conta(cls, cliente, numero):
        conta = cls(
            saldo = 0.0,
            numero = numero,
            agencia = "0001",
            cliente = cliente,
            historico = Historico(),
            limite = 500.0,
            limite_saques = 3
        )
        cliente.adicionar_conta(conta)
        return conta

class ContaCorrente(Conta):
    def __init__ (self, saldo, numero, agencia, cliente, historico, limite, limite_saques):
        super().__init__ (saldo, numero, agencia, cliente, historico)
        self.limite = limite                
        self.limite_saques = limite_saques  
        self.saques_realizados = 0          

    def sacar(self, valor):
        if valor > self.limite:
            print(f"Erro: valor máximo por saque é R${self.limite:.2f}.")
            return False
        if self.saques_realizados >= self.limite_saques:
            print("Erro: número máximo de saques diários atingido.")
            return False
        if valor > self.saldo:
            print("Valor indisponível.")
            return False
        
        self.saldo -= valor
        self.saques_realizados += 1
        print(f"Saque de R${valor:.2f} realizado com sucesso.")
        return True


class Historico:
    def __init__ (self):

        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

    def gerar_relatorio(self, tipo_transacao = None):
        for transacao in self.transacoes:
            tipo = transacao.__class__.__name__
            if tipo_transacao is None or tipo == tipo_transacao:
                print(f"{tipo}: R${transacao.valor:.2f}")
        pass

class TransacaoInterface(ABC): 

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(TransacaoInterface):
    def __init__ (self, valor):
        self.valor = valor

    @log_transacao
    def registrar(self, conta):
        if conta.depositar(self.valor):  
            conta.historico.adicionar_transacao(self)

class Saque(TransacaoInterface):
    def __init__ (self, valor):
        self.valor = valor

    @log_transacao
    def registrar(self, conta):
        if conta.sacar(self.valor):  
            conta.historico.adicionar_transacao(self)

class ContaIterador:
    def __init__(self, contas):
        self.contas = contas
        self.indice = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.indice >= len(self.contas):
            raise StopIteration
        conta = self.contas[self.indice]
        self.indice += 1
        return conta

#=========================================Funcionamento====================================================#
print("""
        ----------------------------------------------
        || Bem-Vindo(a) ao aplicativo do banco DIO! || 
        ----------------------------------------------\n""")

clientes = []
contas = []

def menu():
    print("""
          Selecione uma operação a ser realizada: 
        1 - Depósito 
        2 - Saque 
        3 - Verificar Extrato
        4 - Criar Novo Usuário
        5 - Criar Nova Conta 
        6 - Listar Contas
        0 - Sair do Aplicativo
    """)
    return input("Informe com um dos números mostrados acima: ")

def filtrar_usuario(cpf):
    for cliente in clientes:
        if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf:
            return cliente
    return None

@log_transacao
def criar_usuario():
    cpf = input("Informe o CPF (somente números): ")
    if filtrar_usuario(cpf):
        print("\nJá existe um usuário com esse CPF.")
        return None
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento no formato 'dd/mm/aaaa': ")
    endereco = input("Informe o endereço no formato 'Logradouro - Nº - Bairro - Cidade - Estado': ")
    
    novo_cliente = PessoaFisica(endereco, cpf, nome, data_nascimento)
    clientes.append(novo_cliente)
    print("Usuário criado com sucesso.")
    return novo_cliente

@log_transacao
def criar_conta():
    cpf = input("Informe o CPF do usuário: ")
    cliente = filtrar_usuario(cpf)
    
    if cliente:
        numero_conta = len(contas) + 1
        conta = ContaCorrente.nova_conta(cliente, numero_conta)
        contas.append(conta)
        print("Conta criada com sucesso.")
        return conta
    
    print("Usuário não encontrado.")
    return None

def listar_contas():
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    for conta in ContaIterador(contas):
        print(f"Agência: {conta.agencia} | Número: {conta.numero} | Titular: {conta.cliente.nome}")

def encontrar_conta_por_cpf():
    cpf = input("Informe o CPF do titular da conta: ")
    cliente = filtrar_usuario(cpf)
    if cliente and cliente.contas:
        return cliente.contas[0]  
    print("Conta não encontrada para esse CPF.")
    return None

def exibir_extrato(conta, tipo_extrato):
    print("\n====== Extrato ======")
    if not conta.historico.transacoes:
            print("Não há movimentações.")
    else:
        if tipo_extrato == 1:
            conta.historico.gerar_relatorio("Deposito")
        elif tipo_extrato == 2:
            conta.historico.gerar_relatorio("Saque")
        elif tipo_extrato == 3:
            conta.historico.gerar_relatorio()
        else:
            print("Filtro não reconhecido. Tente novamente.")
    print(f"Saldo atual: R${conta.saldo:.2f}")
    print("=====================")



def main():
    while True:
        acao = menu()

        if acao == "1":
            conta = encontrar_conta_por_cpf()
            if conta:
                try:
                    valor = float(input("Informe o valor a ser depositado: "))
                    deposito = Deposito(valor)
                    conta.cliente.realizar_transacoes(conta, deposito)
                except ValueError:
                    print("Entrada inválida. Tente novamente.")
        
        elif acao == "2":
            conta = encontrar_conta_por_cpf()
            if conta:
                try:
                    valor = float(input("Informe o valor a ser sacado: "))
                    saque = Saque(valor)
                    conta.cliente.realizar_transacoes(conta, saque)
                except ValueError:
                    print("Entrada inválida. Tente novamente.")
        
        elif acao == "3":
            conta = encontrar_conta_por_cpf()
            print("\n   ===|Filtros aplicáveis|===")
            print("""
    Digite: 
        1 - Para visualizar somente seus depósitos;
        2 - Para visualizar somente seus saques;
        3 - Para visualizar todas as operações;
                                     """)
            tipo_extrato = int(input())

            exibir_extrato(conta, tipo_extrato)

        elif acao == "4":
            criar_usuario()

        elif acao == "5":
            criar_conta()

        elif acao == "6":
            listar_contas()

        elif acao == "0":
            print("Obrigado por usar o nosso aplicativo!")
            break

        else:
            print("Operação não identificada. Tente novamente.\n")

if __name__ == "__main__":
    main()
