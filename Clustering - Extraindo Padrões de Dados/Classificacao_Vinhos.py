#%%
import plotly.graph_objects as go 
import pandas as pd 
import numpy as np 

#%%
caminho_arquivo = "Wine.csv"
df = pd.read_csv(caminho_arquivo)
df.head()

# %%
#Passando colunas para português
df = df.rename(columns={
    'Alcohol' : 'Alcool',
    'Ash' : 'Po',
    'Ash_Alcanity' : 'Alcalinidade_po',
    'Magnesium' : 'Magnesio',
    'Color_Intensity' : 'Intensidade de cor'
})

df.head()

# %%
#Informações sobre o dataframe 
df.describe()
# %%
#Matriz de correlação 
matriz_corr = df.corr()
matriz_corr

#%%
#Gráfico de correlação
from biokit.viz import corrplot
import matplotlib.pyplot as plt 

corr_graf = corrplot.Corrplot(matriz_corr)
corr_graf.plot(upper = 'ellipse', fontsize='x-large')
fig = plt.gcf()
fig.set_size_inches(13,8)
fig.show()

#%%
#Normalização manual 
atributos = df.columns
for atributo in atributos:
    df[atributo] = (df[atributo] - min(df[atributo]))/(max(df[atributo]) - min(df[atributo]))

df.head()


#%%
#Normalização SKLearn
from sklearn import preprocessing 
min_max_scaler = preprocessing.MinMaxScaler()
np_df = min_max_scaler.fit_transform(df)
df = pd.DataFrame(np_df, columns= df.columns)

#np_df_inv = min_max_scaler.inverse_transform(df)
#df = pd.DataFrame(np_df_inv, columns= df.columns)

df.describe()

#%% 
#Introdução ao K-means
from sklearn.cluster import KMeans 
agrupador = KMeans(n_clusters=4) #4 número de grupos que serão criados
agrupador.fit(df)

labels = agrupador.labels_
print(labels)

fig = go.Figure()
fig.add_trace(go.Scatter(x = df['Intensidade de cor'], y=df['Alcool'], 
mode='markers', marker=dict(color=agrupador.labels_.astype(np.float)),
text = labels))

fig.show()

#%%
#Exibindo os clusters em 3D
fig = go.Figure()
fig.add_trace(go.Scatter3d(x= df['Intensidade de cor'],
                           y= df['Alcool'],
                           z= df['Proline'],
                           mode='markers',
                           marker=dict(color=labels.astype(np.float)),
                           text=labels))
fig.show()
fig.update_layout(scene= dict(
    xaxis_title = 'Intensidade de Cor',
    yaxis_title = 'Álcool',
    zaxis_title = 'Proline'
))


#%%
'''
K-Means - Não costuma apresentar um bom resultado quando há ruídos e grupos de simetria não radial. 

DBSCAN - Mais adequado quando há ruídos e grupos de simetria não radial.
Ele define uma distância mínima para que os pontos sejam considerados vizinhos, essa distância é chamada de eps.
No nosso caso aqui, ela é um. Além disso, ele define o número mínimo de pontos dentro de um grupo para que isso seja considerado um cluster real.
Ele inicializa em uma amostra aleatória, verifica todos os vizinhos dessa amostra e vai fazendo isso até que ele encontre uma amostra que não tenha
mais vizinhos, ou seja, até ele não possa mais expandir.
'''

#%%
from sklearn.cluster import DBSCAN
agrupador = DBSCAN(eps = 0.5, min_samples=15, metric='euclidean')
agrupador.fit(df)
agrupador.labels_


#%%
#Mean shift 
#Com esse método não precisamos configurar tanta coisa como no DBSCAN
#Diferente do K-Means, ele não requer a especificação do número de clusters e
#assim como o DBScan, procura regiões de alta densidade e afirma que ali existem 
#clusters.

#O contexto geral do Mean shift é buscar regiões de alta densidade de amostras e
#deslocar o centro dos clustes para ela.

#Desvantagens: Não funciona bem com dados de alta dimensionalidade, porque assim como
#outros algoritmos, também usa algumas métricas de distância. 
#Computacionalmente caro.

from sklearn.cluster import MeanShift 
agrupador = MeanShift()
agrupador.fit(df)
agrupador.labels_

#%%
from sklearn.cluster import estimate_bandwidth
BW = estimate_bandwidth(df, quantile=0.1)
agrupador = MeanShift(BW)
agrupador.fit(df)
agrupador.labels_


#%%
#Coeficiente sillueta K-Means
from sklearn.metrics import silhouette_score
faixa_n_clusters = [i for i in range(2,10)]
print(faixa_n_clusters)

from sklearn.cluster import KMeans 

valores_silhueta = []
for k in faixa_n_clusters:
    agrupador = KMeans(n_clusters=k)
    labels = agrupador.fit_predict(df)
    media_silhueta = silhouette_score(df,labels)
    valores_silhueta.append(media_silhueta)

#Note que quando fazemos com apenas um cluster, 
#o K-Means não gera o coeficiente de silhueta.
fig = go.Figure()
fig.add_trace(go.Scatter(x=faixa_n_clusters, y=valores_silhueta))
fig.update_layout(
    title="Valores de Silhueta Médios",
    xaxis_title="Número de Clústeres",
    yaxis_title="Valor Médio de Silhueta"

)
