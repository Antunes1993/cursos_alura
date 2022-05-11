#%%
import pandas as pd
from sklearn.metrics import accuracy_score

dados = pd.read_csv("busca.csv")
# %%
#Pega variáveis categóricas
x = dados[['home','busca','logado']]
y = dados['comprou']

Xdummies = pd.get_dummies(x)
print (Xdummies.head())

#%%
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

SEED = 200
np.random.seed(SEED)
treino_x, teste_x, treino_y, teste_y = train_test_split(Xdummies, y, test_size = 0.25,
                                                         stratify = y)
print("Treinaremos com %d elementos e testaremos com %d elementos" % (len(treino_x), len(teste_x)))

# %%
#Determinação do base line 
from sklearn.dummy import DummyClassifier
dummy = DummyClassifier()
dummy.fit(treino_x, treino_y)
previsoes = dummy.predict(teste_x)

acuracia = accuracy_score(teste_y, previsoes) * 100
print("A acurácia do Dummy foi de %.2f%%" % acuracia)

# %%
from sklearn.naive_bayes import MultinomialNB
modelo = MultinomialNB()
modelo.fit(treino_x, treino_y)
previsoes2 = modelo.predict(teste_x)
acuracia2 = accuracy_score(teste_y, previsoes2) * 100
print("A acurácia do Dummy foi de %.2f%%" % acuracia2)

#%%
from sklearn.ensemble import AdaBoostClassifier

modelo = AdaBoostClassifier()
modelo.fit(treino_x, treino_y)
previsoes2 = modelo.predict(teste_x)
acuracia2 = accuracy_score(teste_y, previsoes2) * 100
print("A acurácia do Dummy foi de %.2f%%" % acuracia2)
# %%
