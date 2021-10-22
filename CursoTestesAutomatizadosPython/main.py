from dominio import Usuario, Lance, Leilao, Avaliador

#Criação de usuários
gui = Usuario('gui')
yuri = Usuario('yuri')

#Criação de lances
lance_do_yuri = Lance(yuri, 100)
lance_do_gui = Lance(gui, 150)

#Criação do objeto leilão
leilao = Leilao('Celular')

#Adição dos lances criados à lista de lances
leilao.lances.append(lance_do_gui)
leilao.lances.append(lance_do_yuri)


for lance in leilao.lances:
    print(f'O usuario {lance.usuario.nome} deu um lance de {lance.valor}')

avaliador = Avaliador()
avaliador.avalia(leilao)

print(f'O menor lance foi de {avaliador.menor_lance} e o maior lance foi de {avaliador.maior_lance}')