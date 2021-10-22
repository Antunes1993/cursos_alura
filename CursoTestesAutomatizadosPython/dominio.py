import sys
#Classe Usuario
class Usuario: 
    def __init__(self, nome):
        self.__nome = nome

    @property
    def nome(self):
        return self.__nome 

#Classe Lance
class Lance:
    def __init__(self, usuario:Usuario, valor):
        self.usuario = usuario
        self.__valor = valor 

    @property
    def valor(self):
        return self.__valor

#Classe Leilao
class Leilao: 
    def __init__(self, descricao):
        self.descricao = descricao
        self.__lances = []

    @property
    def lances(self):
        return self.__lances

#Classe Avaliador 
class Avaliador:
    def __init__(self):
        self.maior_lance = sys.float_info.min 
        self.menor_lance =  sys.float_info.max 
    
    def avalia(self, leilao: Leilao):

        for lance in leilao.lances:
            if lance.valor > self.maior_lance:
                self.maior_lance = lance.valor 
            elif lance.valor < self.menor_lance:
                self.menor_lance = lance.valor



