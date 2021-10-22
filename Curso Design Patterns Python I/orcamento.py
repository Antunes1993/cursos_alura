from impostos import ICMS, ISS

class Orcamento(object):
    def __init__(self, valor):
        self.__valor = valor 

    @property
    def valor(self):
        return self.__valor


class Calculador_impostos(object):
    def realiza_calculo(self, orcamento, imposto):
        valor = imposto.calcula(orcamento)
        print (valor)

class Novo_Orcamento(Object):
    def __init__(self):
        self.__itens = [] 


    @property
    def valor(self):
        total = 0.0
        for item in self.__itens:
            total += item.valor



orcamento01 = Orcamento(5000)
imposto = Calculador_impostos()
imposto.realiza_calculo(orcamento01, ICMS())


