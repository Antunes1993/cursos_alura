from dominio import *

leo = Usuario('Leonardo')
yuri = Usuario('Yuri')
gui = Usuario('Guilherme')

lance_yuri = Lance(yuri, 200)
lance_gui = Lance(gui, 300)
lance_leonardo = Lance(leo, 100)

leilao = Leilao('Celular')
leilao.lances.append(lance_leonardo)
leilao.lances.append(lance_yuri)
leilao.lances.append(lance_gui)


for lance in leilao.lances:
    print (f'O usuário {lance.usuario.nome} de um lance de {lance.valor}')
    

avaliador = Avaliador()
avaliador.avalia(leilao)


print (f'O maior lance foi de {avaliador.maior_lance} e o menor de {avaliador.menor_lance}')
