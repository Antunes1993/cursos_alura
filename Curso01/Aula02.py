#%%
import pandas as pd

uri = "https://gist.githubusercontent.com/guilhermesilveira/1b7d5475863c15f484ac495bd70975cf/raw/16aff7a0aee67e7c100a2a48b676a2d2d142f646/projects.csv"
dados = pd.read_csv(uri)
dados.head()
# %%
renomear = {
    'expected_hours' : 'horas_esperadas',
    'price' : 'preco',
    'unfinished' : 'nao_finalizado',
}

trocar = {
    0:1,
    1:0
}

dados = dados.rename(columns = renomear)
dados['finalizado'] = dados.nao_finalizado.map(trocar)
dados.head(20)

#%%
import seaborn as sns 

sns.scatterplot(x="horas_esperadas", y="preco", hue="finalizado", data=dados)
sns.relplot(x="horas_esperadas", y="preco", hue="finalizado", col="finalizado", data=dados)

# %%
x = dados[['horas_esperadas', 'preco']]
y = dados['finalizado']


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


# %%
import numpy as np 
previsoes_de_base = np.ones(540)
acuracia = accuracy_score(teste_y, previsoes_de_base) * 100
print("Acuráfica foi: %.2f " % acuracia)
