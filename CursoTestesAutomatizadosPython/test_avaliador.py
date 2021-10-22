import unittest
from unittest import TestCase
from dominio import Usuario, Lance, Leilao, Avaliador

class TestAvaliador(TestCase):
    def setUp(self):
        #Criação de usuários
        self.gui = Usuario('Gui')
        self.yuri = Usuario('Yuri')
        self.leonardo = Usuario('Leonardo')

        #Criação de lances
        self.lance_do_yuri = Lance(self.yuri, 100.0)
        self.lance_do_gui = Lance(self.gui, 150.0)
        self.lance_do_leonardo = Lance(self.leonardo, 200.0)

        #Criação do objeto leilão
        self.leilao = Leilao('Celular')

   
    def test_avalia(self):
       
        #Adição dos lances criados à lista de lances
        self.leilao.lances.append(self.lance_do_gui)
        self.leilao.lances.append(self.lance_do_yuri)
        self.leilao.lances.append(self.lance_do_leonardo)

        avaliador = Avaliador()
        avaliador.avalia(self.leilao)

        menor_valor_esperado = 100.0
        maior_valor_esperado = 150.0

        self.assertEqual(menor_valor_esperado, avaliador.menor_lance)
        self.assertEqual(maior_valor_esperado, avaliador.maior_lance)


if ( __name__ == "__main__"):
    unittest.main()