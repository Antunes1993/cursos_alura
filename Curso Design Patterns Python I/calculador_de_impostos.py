# %%
from impostos import ICMS, ISS

class Calculador_de_Impostos(object):
    def realiza_calculo(self, orcamento, imposto):
        #Duck typing - Posso receber qualquer objeto que implemente a função calcula
        imposto_calculado = imposto.calcula(orcamento)
        print(imposto_calculado)





# %%
if __name__ == '__main__':
    from orcamento import Orcamento 

    calculador = Calculador_de_Impostos()
    orcamento = Orcamento(500)
    
    #1. Funções são cidadões de primeira classe
    calculador.realiza_calculo(orcamento, ISS())
    calculador.realiza_calculo(orcamento, ICMS())





