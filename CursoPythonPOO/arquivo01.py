#Revisão curso Python 3 - Avançando orientação a objetos 

# %%
class Programa:
        def __init__(self, titulo, ano, genero):
            self._titulo = titulo.title()
            self.ano = ano
            self.genero = genero
            self._like = 0

        def dar_like(self):
            self._like += 1

        @property
        def titulo(self):
            return self._titulo

        @property
        def like(self):
            return self._like

        def __str__(self):
                return f'{self.titulo} - {self.ano} - {self.genero} - {self.like} - {self.temporadas} temporadas'

class Filme(Programa):
    def __init__(self, titulo, ano,duracao, genero):
        super().__init__(titulo, ano, genero)
        self.duracao = duracao
        
    def __str__(self):
        return f'{self.titulo} - {self.ano} - {self.genero} - {self.like} - {self.duracao} min'

class Serie(Programa):
    def __init__(self, titulo, ano,temporadas, genero):
        super().__init__(titulo, ano, genero)
        self.temporadas = temporadas        

    def __str__(self):
        return f'{self.titulo} - {self.ano} - {self.genero} - {self.like} - {self.temporadas} temporadas'

class PlayList(list):
    def __init__(self, nome, programas):
        self.nome = nome
        self.programas = programas
    
    def __str__(self):
        return f'{self.nome} - {len(self.programas)} programas'  

    def __add__(self, outra_playlist):
        self.programas += outra_playlist.programas
        return self

    @property
    def tamanho(self):
        return len(self.programas)
    

# %%

#Filmes
vingadores = Filme("vingadores - guerra infinita", 2018, 160, "acao")
capitao_phillips = Filme("capitao phillips", 2019, 120, "drama")

#Series
friends = Serie("friends", 2019, 10, "comedia")
tbbt = Serie("tbbt", 2018, 10, "comedia")
demolidor = Serie("demolidor", 2018, 10, "drama")

print ("Filmes e séries criados.")
programas = [vingadores,capitao_phillips,friends,tbbt, demolidor]



# %%
#Coesão de polimorfismo
for programa in programas:
    print(programa)


# %%

#Criando uma playlist 1
fim_de_semana = PlayList("fim de semana", programas)

print ("Primeira PlayList")
for item in fim_de_semana.programas:
    print(item)


# %%

#Criando uma playlist 2
#Filmes
todo_poderoso = Filme("Todo Poderoso", 2018, 160, "comedia")
sim_senhor = Filme("Sim Senhor", 2019, 120, "comedia")
programas2 = [todo_poderoso, sim_senhor]



fim_de_semana_2 = PlayList("fim de semana 2", programas2)

print ("Segunda PlayList")
for item in fim_de_semana_2.programas:
    print(item)

# %%

fim_de_semana = fim_de_semana + fim_de_semana_2
for item in fim_de_semana.programas:
    print(item)

