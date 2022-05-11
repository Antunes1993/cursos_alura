#%%
import pandas as pd
from sklearn.metrics import accuracy_score

uri = "https://gist.githubusercontent.com/guilhermesilveira/2d2efa37d66b6c84a722ea627a897ced/raw/10968b997d885cbded1c92938c7a9912ba41c615/tracking.csv"
dados = pd.read_csv(uri)
# %%
x = dados[["home", "how_it_works", "contact"]]
y = dados["bought"]

treino_x = x[:75]
treino_y = y[:75]

teste_x = x[75:]
teste_y = y[75:]

#%%
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score

modelo = LinearSVC()
modelo.fit(treino_x, treino_y)
previsoes = modelo.predict(teste_x)

taxa_acerto = accuracy_score(teste_y, previsoes) * 100
print("Acuráfica foi: %.2f " % taxa_acerto)

#%%
from sklearn.model_selection import train_test_split
treino_x, teste_x, treino_y, teste_y = train_test_split(x, y, stratify= y, test_size=0.25, random_state=80)
print(treino_x.shape)
print(teste_x.shape)

from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score

modelo = LinearSVC()
modelo.fit(treino_x, treino_y)
previsoes = modelo.predict(teste_x)

taxa_acerto = accuracy_score(teste_y, previsoes) * 100
print("Acuráfica foi: %.2f " % taxa_acerto)