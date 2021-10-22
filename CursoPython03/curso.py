#########################################################
#               CURSO PYTHON 3 - ALURA
#
#   Curso: Python Orientação a objetos.
#   Assunto: Classes, getters, setters, property
#
#
#########################################################

class Conta: 

    def __init__(self, numero, titular, saldo, limite):
        print("Construindo objeto... {}".format(self))
        self.numero = numero 
        self.titular = titular
        self.saldo = saldo 
        self.limite = limite 

    def extrato(self):
        print("Saldo de {} do titular {}".format(self.saldo, self.titular))

    def deposita(self, valor):
        self.saldo += valor 

    def saca(self, valor):
        if(valor <= (self.saldo + self.limite)):
            self.saldo -= valor
        else:
            print ("O valor {} passou o limite.".format(valor))


    def transfere(self, valor, origem, destino):
        origem.saca(valor)
        destino.deposita(valor)

    def get_saldo(self):
        return self.saldo

    @property
    def nome(self):
        print("Chamando @property nome{}")
        return self.titular.title()

    @nome.setter
    def nome(self, titular):
        print("Chamando @setter nome{}")
        self.titular = titular        

    @property
    def valorLimite(self):
        print("Chamando @property limite{}")
        return self.limite

    @valorLimite.setter
    def valorLimite(self, limite):
        print("Chamando @setter limite{}")
        self.limite = limite     

conta1 = Conta(123, "Leonardo", 55.5, 1000.0)
conta2 = Conta(123, "Leticia", 155.5, 1000.0)


print (conta1.nome)
print (conta1.limite)

conta1.nome = "Leticia"
conta1.limite = 2000
print (conta1.nome)
print (conta1.limite)

conta1.saca(4000)
