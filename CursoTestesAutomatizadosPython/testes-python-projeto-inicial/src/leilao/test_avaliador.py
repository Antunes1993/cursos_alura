from unittest import TestCase
from dominio import Usuario, Lance, Leilao, Avaliador

class TestAvaliador(TestCase):
    #Método setUp sempre invocado no começo dos testes
    def setUp(self):
        self.gui = Usuario('Gui')
        self.yuri = Usuario('Yuri')
        self.lance_do_yuri = Lance(self.yuri, 100)
        self.lance_do_gui = Lance(self.gui, 150)
        self.leilao = Leilao('Celular')


    def test_avalia_lance_crescente(self):
        self.leilao.propoe(self.lance_do_yuri)
        self.leilao.propoe(self.lance_do_gui)

        avaliador = Avaliador()
        avaliador.avalia(self.leilao)

        menor_valor_esperado = 100
        maior_valor_esperado = 150

        self.assertEqual(menor_valor_esperado, avaliador.menor_lance)
        self.assertEqual(maior_valor_esperado, avaliador.maior_lance)


    def test_avalia_lance_decrescente(self):


        self.leilao.propoe(self.lance_do_yuri)
        self.leilao.propoe(self.lance_do_gui)

        avaliador = Avaliador()
        avaliador.avalia(self.leilao)

        maior_valor_esperado = 150
        menor_valor_esperado = 100

        self.assertEqual(menor_valor_esperado, avaliador.menor_lance)
        self.assertEqual(maior_valor_esperado, avaliador.maior_lance)


    def test_avalia_lance_caso_onde_so_haja_um_lance(self):
        self.leilao.propoe(self.lance_do_gui)

        avaliador = Avaliador()
        avaliador.avalia(self.leilao)

        maior_valor_esperado = 150
        menor_valor_esperado = 150

        self.assertEqual(menor_valor_esperado, avaliador.menor_lance)
        self.assertEqual(maior_valor_esperado, avaliador.maior_lance)

    def test_permitir_propor_lance_caso_leilao_nao_tenha_lances(self):
        self.leilao.propoe(self.lance_do_gui)
        self.assertEqual(1, len(self.leilao.lances))


    def test_nao_permitir_propor_lance_caso_usuario_seja_o_mesmo(self):
        lance_do_gui200 = Lance(self.yuri, 200.0)

        self.leilao.propoe(self.lance_do_gui)
        self.leilao.propoe(lance_do_gui200)

        quantidade_de_lances_recebidos = len(self.leilao.lances)
        self.assertEqual(2, quantidade_de_lances_recebidos)

