
from unittest import TestCase
from leilao.dominio import *

class TestLeilao(TestCase):
    def setUp(self):
        self.leo = Usuario('Leonardo')
        self.gui = Usuario('Guilherme')
        self.yuri = Usuario('Yuri')

        self.lance_gui = Lance(self.gui, 200)
        self.lance_leonardo = Lance(self.leo, 100)
        self.lance_yuri = Lance(self.yuri, 300)

        self.leilao = Leilao('Celular')

    def test_avalia_um_ou_mais_lances(self):
        self.leilao.propoe(self.lance_leonardo)
        self.leilao.propoe(self.lance_gui)
        self.leilao.propoe(self.lance_yuri)

        menor_valor_esperado = 100
        maior_valor_esperado = 300

        self.assertEqual(menor_valor_esperado, self.leilao.menor_lance)
        self.assertEqual(maior_valor_esperado, self.leilao.maior_lance)

    def teste_retorna_mesmo_valor_quando_leilao_tem_um_lance(self):
        self.leilao.propoe(self.lance_leonardo)

        menor_valor_esperado = 100
        maior_valor_esperado = 100

        self.assertEqual(menor_valor_esperado, self.leilao.menor_lance)
        self.assertEqual(maior_valor_esperado, self.leilao.maior_lance)

    def teste_deve_permitir_propor_lance_caso_leilao_nao_tenha_lance(self):
        self.leilao.propoe(self.lance_leonardo)
        self.assertEqual(1, len(self.leilao.lances))


    def test_deve_permitir_propor_um_lance_caso_ultimo_usuario_seja_diferente(self):
        self.leilao.propoe(self.lance_leonardo)
        self.leilao.propoe(self.lance_gui)

        quantidade_lances_recebidos = len(self.leilao.lances)
        self.assertEqual(2, quantidade_lances_recebidos)

    def test_nao_deve_permitir_propor_um_lance_caso_ultimo_usuario_seja_igual(self):
        self.leilao.propoe(self.lance_leonardo)
        #self.leilao.propoe(self.lance_leonardo)
        quantidade_lances_recebidos = len(self.leilao.lances)
        self.assertEqual(1, quantidade_lances_recebidos) #Se usar o assertRaises, não precisa usar o assert Equal
