#%%
import pandas as pd 
uri = "https://gist.githubusercontent.com/guilhermesilveira/4d1d4a16ccbf6ea4e0a64a38a24ec884/raw/afd05cb0c796d18f3f5a6537053ded308ba94bf7/car-prices.csv"
dados = pd.read_csv(uri)
dados.head()

# %%
#Tratamento dos dados

#Renomear colunas para pt
renomear_portugues = {
    'Unnamed: 0':'id',
    'mileage_per_year':'milhas_por_ano',
    'model_year': 'ano_modelo',
    'price':'preco',
    'sold':'vendido',
}
dados_renomeados = dados.rename(columns = renomear_portugues)

#Conversão da coluna de status de venda para binário
a_trocar = {
    'no' : 0,
    'yes' : 1
}
dados_renomeados.vendido = dados_renomeados.vendido.map(a_trocar)

#Conversão da coluna de ano de modelo para integer
from datetime import datetime
ano_atual = datetime.today().year
dados_renomeados['ano_modelo'] = ano_atual - dados_renomeados.ano_modelo

#Conversão da coluna de quilometragem para quilometros 
dados_renomeados ['quilometragem_por_ano'] = dados_renomeados.milhas_por_ano * 1.60934
dados_renomeados.drop('milhas_por_ano', axis=1)
dados_renomeados.head()

#%%
import seaborn as sns
sns.scatterplot(x="quilometragem_por_ano", y="preco", hue="vendido", data=dados_renomeados)
sns.relplot(x="quilometragem_por_ano", y="preco", hue="vendido", col="vendido", data=dados_renomeados)


#%%

import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

x = dados_renomeados[['preco','quilometragem_por_ano', 'ano_modelo']]
y = dados_renomeados['vendido']

SEED = 200
np.random.seed(SEED)
treino_x, teste_x, treino_y, teste_y = train_test_split(x, y, test_size = 0.25,
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


#%%
#Linear SVC
from sklearn.svm import LinearSVC
modelo = LinearSVC()
modelo.fit(treino_x, treino_y)
previsoes = modelo.predict(teste_x)

acuracia = accuracy_score(teste_y, previsoes) * 100
print("A acurácia foi %.2f%%" % acuracia)

#%%
#SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

scaler = StandardScaler()
scaler.fit(treino_x)
treino_x_s = scaler.transform(treino_x)
teste_x_s = scaler.transform(teste_x)

modelo = SVC()
modelo.fit(treino_x_s, treino_y)
previsoes = modelo.predict(teste_x_s)

acuracia = accuracy_score(teste_y, previsoes) * 100
print("A acurácia foi %.2f%%" % acuracia)


# %%
#Decision tree classifier 
from sklearn.tree import DecisionTreeClassifier
modelo = DecisionTreeClassifier(max_depth=2)
modelo.fit(treino_x, treino_y)
previsoes = modelo.predict(teste_x)
acuracia = accuracy_score(teste_y, previsoes) * 100
print("A acurácia foi %.2f%%" % acuracia)

# %%
#Visualização gráfica do modelo de decisão
from sklearn.tree import export_graphviz
import graphviz

features = x.columns
dot_data = export_graphviz(modelo, out_file=None, feature_names=features, filled=True, rounded=True, special_characters=True, class_names=["não", "sim"])
graph = graphviz.Source(dot_data)
graph.render("tree")
# %%
