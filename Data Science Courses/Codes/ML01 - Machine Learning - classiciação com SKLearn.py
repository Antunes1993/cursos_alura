#%%
#Bibliotecas
import graphviz
import numpy as np
import pandas as pd 
import seaborn as sns
import plotly.express as px
from datetime import datetime
from sklearn.svm import LinearSVC, SVC
from sklearn.tree import export_graphviz
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

#%%

# features (1 sim, 0 não)
# pelo longo? 
# perna curta?
# faz auau?

porco1 = [0, 1, 0]
porco2 = [0, 1, 1]
porco3 = [1, 1, 0]

cachorro1 = [0, 1, 1]
cachorro2 = [1, 0, 1]
cachorro3 = [1, 1, 1]

train_x = [porco1, porco2, porco3, cachorro1, cachorro2, cachorro3]
train_y = [1,1,1,0,0,0]

model = LinearSVC()
model.fit(train_x, train_y)

#Predição individual
novo_animal = [1,1,1]
predicao = (model.predict([novo_animal])[0]) # 1 = porco, 0 = cachorro
mapa = {0: 'Cachorro', 1: 'Porco'}
print(f'O animal é um {mapa[predicao]}')

#Predição multipla
misterio1 = [1,1,1]
misterio2 = [1,1,0]
misterio3 = [0,1,1]

teste_x = [misterio1, misterio2, misterio3]
testes_y = [0, 1, 1]
resultados = model.predict(teste_x) # 1 = porco, 0 = cachorro
for i, resultado in enumerate(resultados):
    print(f'O animal {i+1} é um {mapa[resultado]}')

#Vendo acuracia do modelo

corretos = (resultados == testes_y).sum()
total = len(testes_y)
taxa_acerto = corretos / total * 100
print(f'Taxa de acerto: {taxa_acerto:.2f}%')
#%%
uri = "https://gist.githubusercontent.com/guilhermesilveira/2d2efa37d66b6c84a722ea627a897ced/raw/10968b997d885cbded1c92938c7a9912ba41c615/tracking.csv"
data = pd.read_csv(uri)
data.head()

# Trabalhando com as features em portugues. 
mapa = {
    'home': 'home',
    'how_it_works': 'como funciona',
    'contact': 'contato',
    'bought': 'comprou'
}

data.rename(columns=mapa, inplace=True)


# Ao refletirmos sobre o modelo que estamos adotando, seria mais interessante 
# que a coluna bought fosse separada das outras três, afinal ela corresponde 
# no modelo da função ao y*, enquanto nossas features (home, *howitworks e 
# contact) representam **x.
x = data[['home', 'como funciona', 'contato']]
y = data['comprou']

x.shape, y.shape
x_treino = x[:75]
y_treino = y[:75]
x_teste = x[75:]
y_teste = y[75:]
print(f"Treinaremos com {len(x_treino)}% da base e testaremos com {len(x_teste)}%")

modelo = LinearSVC()
modelo.fit(x_treino, y_treino)
previsoes = modelo.predict(x_teste)
acuracia = accuracy_score(y_teste, previsoes)
print(f"A acurácia do modelo foi de {acuracia:.2%}")

#%%
#Refazendo o exemplo usando metodos da biblioteca sklearn

#O algorítimo train_test_split, por padrão, realiza aleatoriamente a separação
#de dados de treino e teste. Desse modo, todas as vezes que ele é executado 
# podemos ter um resultado diferente.
treino_x, teste_x, treino_y, teste_y = train_test_split(x, y, test_size =0.25)
print(f"Treinaremos com {len(treino_x)}% da base e testaremos com {len(treino_y)}%")

modelo = LinearSVC()
modelo.fit(treino_x, treino_y)
previsoes = modelo.predict(teste_x)
acuracia = accuracy_score(teste_y, previsoes)
print(f"A acurácia do modelo foi de {acuracia:.2%}")

#Tornando o modelo replicável.
SEED = 20

treino_x, teste_x, treino_y, teste_y = train_test_split(x, y, random_state = SEED, test_size = 0.25)
print("Treinaremos com %d elementos e testaremos com %d elementos" % (len(treino_x), len(teste_x)))

modelo = LinearSVC()
modelo.fit(treino_x, treino_y)
previsoes = modelo.predict(teste_x)

acuracia = accuracy_score(teste_y, previsoes) * 100
print("A acurácia foi %.2f%%" % acuracia)

#%%
#Verificando proporcionalidade entre conjuntos.
print(f"{round(treino_y.value_counts()/len(treino_y),2)}")
print(f"{teste_y.value_counts()/len(teste_y)}")

#Caso a separação de conjuntos não esteja proporcional, isso é bem arriscado.
#Por exemplo, se treinarmos apenas com pessoas que não compraram o produto, 
#o algorítimo só saberá que pessoas não compram e esse será o seu palpite 
#padrão pois ele nunca aprendeu que usuários de fato compram o produto.


#Portanto, é importante que a proporção dos nossos dados seja proporcional.
#Para isso,, inseriremos mais um argumento na separação de dados 
#(train_test_split): o stratify = y, que irá estratificar os dados 
#proporcionalmente de acordo com y.
SEED = 20

treino_x, teste_x, treino_y, teste_y = train_test_split(x, y, random_state = SEED, test_size = 0.25, stratify = y)
print("Treinaremos com %d elementos e testaremos com %d elementos" % (len(treino_x), len(teste_x)))

modelo = LinearSVC()
modelo.fit(treino_x, treino_y)
previsoes = modelo.predict(teste_x)

acuracia = accuracy_score(teste_y, previsoes) * 100
print("A acurácia foi %.2f%%" % acuracia)


#%% Terceiro Projeto - Sites finalizados ou nao.
data = pd.read_csv("../Data/ML01 - Classificação por trás dos panos/projects.csv")
data.head()

map = {
    'unfinished': 'nao_finalizado',
    'expected_hours': 'horas esperadas',
    'price': 'preco'
}

data.rename(columns=map, inplace=True)
data.head()

troca = {
    0: 'Finalizado', 
    1: 'Não Finalizado'
}

data['finalizado'] = data['nao_finalizado'].map(troca)
data.drop(columns='nao_finalizado', inplace=True)
data.head()


#%%
#sns.scatterplot(data=data, x='horas esperadas', y='preco', hue='finalizado')


# Gráfico moderno com Plotly
fig = px.scatter(
    data,
    x='horas esperadas',
    y='preco',
    color='finalizado',
    color_discrete_map={
        'Finalizado': 'royalblue',
        'Não Finalizado': 'lightblue'
    },   
    labels={'finalizado': 'Finalizado'},
    title='Relação entre Horas Esperadas e Preço'
)
fig.show()


#%%
x = data[['horas esperadas', 'preco']]
y= data['finalizado']
SEED = 20

treino_x, teste_x, treino_y, teste_y = train_test_split(x, y,
                                                         random_state = SEED, test_size = 0.25,
                                                         stratify = y)
print("Treinaremos com %d elementos e testaremos com %d elementos" % (len(treino_x), len(teste_x)))


modelo = LinearSVC()
modelo.fit(treino_x, treino_y)
previsoes = modelo.predict(teste_x)

acuracia = accuracy_score(teste_y, previsoes) * 100
print("A acurácia foi %.2f%%" % acuracia)
#%%
#A acurácia não parece ser boa, mas essa é a base de um algoritmo 
#para tentar prever resultados. Mas devemos nos perguntar: 
#como saber se 54% é de fato ruim?

#Para obtermos uma resposta satisfatória, precisamos de um recurso
#comparativo. Portanto, inventaremos um algoritmo bem simples que
#terá como previsão que todos os projetos são finalizados, isto é,
#os 540 elementos de teste serão 1.

#Com o Numpy, a biblioteca que gera matrizes, faremos com que 
#540 elementos tenham o valor 1. Feito isso, estipularemos que 
#essas são as previsões, as chamaremos de previsoes_do_leonardo, 
# e testaremos sua acurácia.
previsoes_do_leonardo = np.ones(540)
for item in previsoes_do_leonardo:
    if item == 1:
        item = 'Finalizado'

acuracia = accuracy_score(teste_y, previsoes_do_leonardo) * 100
print("A acurácia do Leonardo foi %.2f%%" % acuracia)

#Ou seja, com esse algoritmo simples, tivemos um resultado de 52.59%
#- um valor muito próximo ao do algoritmo anterior.

#O que chamamos de previsoes_do_guilherme, na verdade é a linha de base,
#ou baseline, e é o parâmetro que devemos superar quando construímos 
#estimadores. Devemos ser muito melhores que as porcentagens apresentadas
#na baseline, e por isso é muito importante que ele exista ainda que teste
#sempre a mesma classe.


#%% Analisando as classificações que fizemos. 
resultado = teste_x.copy()
resultado['real'] = teste_y
resultado['previsao'] = previsoes
resultado['correto'] = resultado['real'] == resultado['previsao']


# Gráfico. Podemos ver que o modelo esta prevendo tudo como finalizado.
# Isso é um problema, pois o modelo não está aprendendo nada.
fig = px.scatter(
    resultado,
    x='horas esperadas',
    y='preco',
    color='previsao',    
    color_discrete_map={True: 'royalblue', False: 'lightblue'},
    title='Classificações do Modelo',
    labels={'correto': 'Classificação correta?', 'status': 'Status real'}
)
fig.show()



#%%
#Estimadores não lineares e Support Vector Machine (SVM)
#O modelo LinearSVC é um estimador linear, ou seja, ele tenta encontrar uma
# reta que separe os dados.
#No entanto, existem dados que não podem ser separados por uma reta.
print("Treinaremos com %d elementos e testaremos com %d elementos" % (len(treino_x), len(teste_x)))

modelo = LinearSVC(random_state=SEED)
modelo.fit(treino_x, treino_y)
previsoes = modelo.predict(teste_x)

acuracia = accuracy_score(teste_y, previsoes) * 100
print("A acurácia foi %.2f%%" % acuracia)


#Usando np.random.seed do numpy, podemos garantir que o resultado sera igual
#Isso porque o LinearSVC toma automaticamente o valor do SEED do numpy.
SEED = 5
np.random.seed(SEED)
treino_x, teste_x, treino_y, teste_y = train_test_split(x, y, test_size = 0.25,
                                                         stratify = y)
print("Treinaremos com %d elementos e testaremos com %d elementos" % (len(treino_x), len(teste_x)))



#%%Usando estimadores não lineares (SVC)
SEED = 5
np.random.seed(SEED)
raw_treino_x, raw_teste_x, treino_y, teste_y = train_test_split(x, y, test_size = 0.25,
                                                         stratify = y)
print("Treinaremos com %d elementos e testaremos com %d elementos" % (len(treino_x), len(teste_x)))

scaler = StandardScaler()
scaler.fit(raw_treino_x)
treino_x = scaler.transform(raw_treino_x)
teste_x = scaler.transform(raw_teste_x)

modelo = SVC()
modelo.fit(treino_x, treino_y)
previsoes = modelo.predict(teste_x)

acuracia = accuracy_score(teste_y, previsoes) * 100
print("A acurácia foi %.2f%%" % acuracia)


#%%
#Quarto Projeto - Venda de carros.
uri = "https://gist.githubusercontent.com/guilhermesilveira/4d1d4a16ccbf6ea4e0a64a38a24ec884/raw/afd05cb0c796d18f3f5a6537053ded308ba94bf7/car-prices.csv"
dados = pd.read_csv(uri)
dados.head()

map = {
    'mileage_per_year': 'millas_por_ano',
    'model_year': 'ano_modelo',
    'price': 'preco',
    'sold': 'vendido'
}

a_trocar = {
    'no': 0,
    'yes': 1
}


dados.rename(columns=map, inplace=True)
dados.vendido = dados.vendido.map(a_trocar)
dados.head()

#%%
#Aqui entra uma reflexao importante. O que é mais importante, o ano do modelo ou 
#ou quantos anos tem o carro?
#Nesse sentido, vamos calcular a idade do carro em vez de usar o ano do modelo.
ano_atual = datetime.now().year
dados['idade_do_modelo'] = ano_atual - dados['ano_modelo']

#Convertendo milhas por ano para km por ano.
dados['km_por_ano'] = dados['millas_por_ano'] * 1.60934

x = dados[['km_por_ano', 'idade_do_modelo']]
y = dados['vendido']


#%%Usando estimadores não lineares (SVC)
SEED = 20
np.random.seed(SEED)
raw_treino_x, raw_teste_x, treino_y, teste_y = train_test_split(x, y, test_size = 0.10,
                                                         stratify = y)
print("Treinaremos com %d elementos e testaremos com %d elementos" % (len(treino_x), len(teste_x)))

scaler = StandardScaler()
scaler.fit(raw_treino_x)
treino_x = scaler.transform(raw_treino_x)
teste_x = scaler.transform(raw_teste_x)

modelo = SVC()
modelo.fit(treino_x, treino_y)
previsoes = modelo.predict(teste_x)

acuracia = accuracy_score(teste_y, previsoes) * 100
print("A acurácia foi %.2f%%" % acuracia)


#Baseline
previsoes_do_leonardo = np.ones(len(teste_y))
for item in previsoes_do_leonardo:
    if item == 1:
        item = 'Finalizado'

acuracia = accuracy_score(teste_y, previsoes_do_leonardo) * 100
print("A acurácia do Baseline Leonardo foi %.2f%%" % acuracia)


dummy = DummyClassifier(strategy='stratified')
dummy.fit(treino_x, treino_y)
previsoes = dummy.predict(teste_x)

acuracia = accuracy_score(teste_y, previsoes) * 100
print("A acurácia do dummy foi %.2f%%" % acuracia)


#%% Testando Tree Classifier
modelo = DecisionTreeClassifier()
modelo.fit(treino_x, treino_y)
previsoes = modelo.predict(teste_x)

acuracia = accuracy_score(teste_y, previsoes) * 100
print("A acurácia foi %.2f%%" % acuracia)