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
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_validate 
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
#%%



uri = "https://gist.githubusercontent.com/guilhermesilveira/4d1d4a16ccbf6ea4e0a64a38a24ec884/raw/afd05cb0c796d18f3f5a6537053ded308ba94bf7/car-prices.csv"
dados = pd.read_csv(uri)
map = {
    'mileage_per_year': 'millas_por_ano',
    'model_year': 'ano_modelo',
    'price': 'preco',
    'sold': 'vendido'}

a_trocar = {
    'no': 0,
    'yes': 1}

dados.rename(columns=map, inplace=True)
dados.vendido = dados.vendido.map(a_trocar)
ano_atual = datetime.now().year
dados['idade_do_modelo'] = ano_atual - dados['ano_modelo']

#Convertendo milhas por ano para km por ano.
dados['km_por_ano'] = dados['millas_por_ano'] * 1.60934
dados.drop(columns=['millas_por_ano', 'ano_modelo'], inplace=True)


x = dados[['km_por_ano', 'idade_do_modelo']]
y = dados['vendido']

dados.rename(columns=map, inplace=True)
dados.head()


#%% Separando dados de treino e teste
SEED = np.random.seed(301)
x_treino, x_teste, y_treino, y_teste = train_test_split(x, y, test_size=0.15, random_state=SEED, stratify=y)
print(f"Treinaremos com {len(x_treino)} e testaremos com {len(x_teste)}")
print(f"Proporção de 0s e 1s no treino: {y_treino.value_counts(normalize=True)}")
print(f"Proporção de 0s e 1s no teste: {y_teste.value_counts(normalize=True)}")

#Dummy Classifier
dummy_stratified = DummyClassifier(strategy='stratified', random_state=SEED)
dummy_stratified.fit(x_treino, y_treino)
y_pred = dummy_stratified.predict(x_teste)
acuracia_dummy = dummy_stratified.score(x_teste, y_teste) * 100
print(f"Acurácia do Dummy Classifier: {round(acuracia_dummy,2)}%")


#SVC
model_svc = SVC(random_state=SEED)
model_svc.fit(x_treino, y_treino)
y_pred = model_svc.predict(x_teste)
acuracia_svc = accuracy_score(y_teste, y_pred) * 100
print(f"Acurácia do SVC: {round(acuracia_svc,2)}%")

#Decision Tree Classifier
model_dtc = DecisionTreeClassifier(random_state=SEED, max_depth=3)
model_dtc.fit(x_treino, y_treino)
y_pred = model_dtc.predict(x_teste)
acuracia_dtc = accuracy_score(y_teste, y_pred) * 100
print(f"Acurácia do Decision Tree Classifier: {round(acuracia_dtc,2)}%")


#%% Validação Cruzada
cv = 5
modelo = DecisionTreeClassifier(max_depth=2)
results = cross_validate(modelo, x, y, cv = cv, return_train_score=False)
media = results['test_score'].mean()
desvio_padrao = results['test_score'].std()

print(f"Acurácia méida: {round(media * 100,2)}%")
print(f"Desvio padrão: {round(desvio_padrao * 100,2)}%")
print(f"Accuracy com crossvalidation {cv}: [%.2f, %.2f]" % ((media - 2 *desvio_padrao) * 100, (media + 2 * desvio_padrao) * 100))


#%% Validação Cruzada com KFold e Shuffle
cv = KFold(n_splits=10, shuffle=True, random_state=SEED)
modelo = DecisionTreeClassifier(max_depth=2)
results = cross_validate(modelo, x, y, cv = cv, return_train_score=False)
media = results['test_score'].mean()
desvio_padrao = results['test_score'].std()

print(f"Acurácia méida: {round(media * 100,2)}%")
print(f"Desvio padrão: {round(desvio_padrao * 100,2)}%")
print(f"Accuracy com crossvalidation {cv}: [%.2f, %.2f]" % ((media - 2 *desvio_padrao) * 100, (media + 2 * desvio_padrao) * 100))

#%% Estratificando os dados com validação cruzada. 
#No crossvalidation, o KFold não estratifica os dados.
#O StratifiedKFold faz isso.
cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=SEED)
modelo = DecisionTreeClassifier(max_depth=2)
results = cross_validate(modelo, x, y, cv = cv, return_train_score=False)
media = results['test_score'].mean()
desvio_padrao = results['test_score'].std()

print(f"Acurácia méida: {round(media * 100,2)}%")
print(f"Desvio padrão: {round(desvio_padrao * 100,2)}%")
print(f"Accuracy com crossvalidation {cv}: [%.2f, %.2f]" % ((media - 2 *desvio_padrao) * 100, (media + 2 * desvio_padrao) * 100))

'''
A estratificação não depende da ordem dos dados, mas sim da proporção das classes em cada divisão.
Quando você usa shuffle=True, o StratifiedKFold:
 + embaralha os dados antes de fazer as divisões,
 + mantém a proporção de classes em cada fold,
 + ajuda a evitar viés causado pela ordenação original dos dados (que é comum em conjuntos reais, 
 como arquivos CSV organizados por tempo, ID, etc.).
'''

