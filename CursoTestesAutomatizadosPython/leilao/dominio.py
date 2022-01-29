import sys
class Usuario: 
    def __init__(self, nome):
        self.__nome = nome

    @property
    def nome(self):
        return self.__nome


class Lance: 
    def __init__(self, usuario, valor):
        self.usuario = usuario
        self.valor = valor

class Leilao: 
    def __init__ (self, descricao):
        self.__lances = []
        self.maior_lance = 0.0
        self.menor_lance = 10000.0

    def propoe(self, lance: Lance):

        if not self._tem_lances() or self._usuarios_diferentes(lance):
            self.lances.append(lance)

            if lance.valor > self.maior_lance:
                self.maior_lance = lance.valor
            if lance.valor < self.menor_lance:
                self.menor_lance = lance.valor
        else:
            raise ValueError("O mesmo usuário não pode propor dois lances seguidos.")

    @property
    def lances(self):
        return self.__lances

    def _tem_lances(self):
        return self.__lances

    def _usuarios_diferentes(self, lance):
        return self.lances[-1].usuario != lance.usuario