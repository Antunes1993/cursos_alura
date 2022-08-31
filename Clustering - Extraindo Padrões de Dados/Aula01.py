#%%
import pandas as pd
from sklearn import cluster 
data = pd.read_csv("CC GENERAL.csv")
data.drop(columns=['CUST_ID', 'TENURE'], inplace=True)
data.head()

missing = data.isna().sum()
print(missing)

#Substituindo os valores faltantes pela mediana de cada atributo. 
data.fillna(data.median(), inplace=True)
missing = data.isna().sum()
print(missing)


#Normalizando os dados
from sklearn.preprocessing import Normalizer 
values = Normalizer().fit_transform(data.values)
values

from sklearn.cluster import KMeans 
kmeans = KMeans(n_clusters=5, n_init=10, max_iter=300)
y_pred = kmeans.fit_predict(values)

#%%
#Metricas de validacao 
#1.Externas (Precisamos ter os labels)
#2.Internas (Nao precisamos ter labels)


#Metricas de validacao internas 
#Criterios:
#Compactação - Diz o quao proximo estão as amostras de cada cluster.
#Separação - Quão bem separados estão os pontos em clusters diferentes (Quão distantes 
# estão os clusters um do outro).

#Métricas: 
# Coeficiente de Silhouette 
# s = (b-a) / max(a,b)
#a  = distancia media entre o ponto e todos os outros pontos do mesmo cluster. 
#Basicamente estamos vendo a compactação. 