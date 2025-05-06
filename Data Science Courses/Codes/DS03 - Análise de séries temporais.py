#%% Class 01 
# Import Libraries
import numpy as np 
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pandas.plotting import autocorrelation_plot


alucar = pd.read_csv("..\\Data\\DS03 - Análise de séries temporais\\alucar.csv", delimiter=',')

#Commands to see rows and columns 
print(f'Quantidade de linhas {alucar.shape[0]} e colunas {alucar.shape[1]}')

#Command to see quantity of null data
print(f'Quantidade de dados nulos: {alucar.isna().sum().sum()}')

#Command to see the type of each data
alucar.dtypes

#Converting month data to datetime
alucar.mes = pd.to_datetime(alucar.mes)
alucar.dtypes

#Visualization
fig = px.line(alucar, x='mes', y='vendas')
fig.update_layout(template='plotly_dark', title='Vendas Alucar de 2017 e 2018', title_x=0.5)
fig.show()



#%% Class 02
#Checking the raise in the sales
alucar['aumento'] = alucar['vendas'].diff()
alucar.head()

#Visualization
fig = px.line(alucar, x='mes', y='aumento')
fig.update_layout(template='plotly_dark', title='Aumento das vendas Alucar de 2017 e 2018', title_x=0.5)
fig.show()

#Check the acceleration in the raise
alucar['aceleracao'] = alucar['aumento'].diff()
alucar.head()

#Visualization
fig = px.line(alucar, x='mes', y='aceleracao')
fig.update_layout(template='plotly_dark', title='Aceleração das vendas Alucar de 2017 e 2018', title_x=0.5)
fig.show()

#Merging the graphs in one image
fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    subplot_titles=[
        'Vendas Alucar 2017 e 2018',
        'Aumento das Vendas',
        'Aceleração das Vendas'
    ]
)

fig.add_trace(go.Scatter(x=alucar['mes'], y=alucar['vendas'], mode='lines', name='Vendas'), row=1, col=1)
fig.add_trace(go.Scatter(x=alucar['mes'], y=alucar['aumento'], mode='lines', name='Aumento'), row=2, col=1)
fig.add_trace(go.Scatter(x=alucar['mes'], y=alucar['aceleracao'], mode='lines', name='Aceleração'), row=3, col=1)

fig.update_layout(
    template='plotly_dark',  # Tema escuro
    height=900,  # Altura da figura
    title_text='Análise das Vendas Alucar de 2017 e 2018',  # Título geral
    title_x=0.5  # Centralizando o título
)

fig.show()

#Autocorrelation Analysis
autocorrelation_plot(alucar['vendas'])



#%% Class 03 
assinantes = pd.read_csv("..\\Data\\DS03 - Análise de séries temporais\\newsletter_alucar.csv", delimiter=',')
print('Quantidade de dados nulos:', assinantes.isna().sum().sum())
assinantes['mes'] = pd.to_datetime(assinantes['mes'])
assinantes
#Checking the raise of subscribers 
assinantes['aumento'] = assinantes['assinantes'].diff()

#Checking the acceleration of the raise of subscreibers
assinantes['aceleracao'] = assinantes['aumento'].diff()

#Merging the graphs in one image
fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    subplot_titles=[
        'Vendas Alucar 2017 e 2018',
        'Aumento das assinantes',
        'Aceleração de aumento de assinantes'
    ]
)

fig.add_trace(go.Scatter(x=assinantes['mes'], y=assinantes['assinantes'], mode='lines', name='Vendas'), row=1, col=1)
fig.add_trace(go.Scatter(x=assinantes['mes'], y=assinantes['aumento'], mode='lines', name='Aumento'), row=2, col=1)
fig.add_trace(go.Scatter(x=assinantes['mes'], y=assinantes['aceleracao'], mode='lines', name='Aceleração'), row=3, col=1)

fig.update_layout(
    template='plotly_dark',  # Tema escuro
    height=900,  # Altura da figura
    title_text='Análise das Vendas Alucar de 2017 e 2018',  # Título geral
    title_x=0.5  # Centralizando o título
)

fig.show()


#%% Sazonality Analysis
chocolura = pd.read_csv("..\\Data\\DS03 - Análise de séries temporais\\chocolura.csv", delimiter=',')
chocolura['mes'] = pd.to_datetime(chocolura['mes'])
chocolura.dtypes
print(f"Quantidade de dados nulos: {chocolura.isna().sum().sum()}")

#Checking the raise of sales 
chocolura['aumento'] = chocolura['vendas'].diff()

#Checking the acceleration of the raise of sales
chocolura['aceleracao'] = chocolura['aumento'].diff()

#Merging the graphs in one image
fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    subplot_titles=[
        'Vendas Alucar 2017 e 2018',
        'Aumento das assinantes',
        'Aceleração de aumento de assinantes'
    ]
)

fig.add_trace(go.Scatter(x=chocolura['mes'], y=chocolura['vendas'], mode='lines', name='Vendas'), row=1, col=1)
fig.add_trace(go.Scatter(x=chocolura['mes'], y=chocolura['aumento'], mode='lines', name='Aumento'), row=2, col=1)
fig.add_trace(go.Scatter(x=chocolura['mes'], y=chocolura['aceleracao'], mode='lines', name='Aceleração'), row=3, col=1)

fig.update_layout(
    template='plotly_dark',  # Tema escuro
    height=900,  # Altura da figura
    title_text='Análise das Vendas Alucar de 2017 e 2018',  # Título geral
    title_x=0.5  # Centralizando o título
)

fig.show()

#%% Class 04
alucel = pd.read_csv("..\\Data\\DS03 - Análise de séries temporais\\alucel.csv", delimiter=',')
alucel['dia'] = pd.to_datetime(alucel['dia'])
alucel.dtypes
print(f"Quantidade de dados nulos: {alucel.isna().sum().sum()}")

#Checking the raise of sales 
alucel['aumento'] = alucel['vendas'].diff()

#Checking the acceleration of the raise of sales
alucel['aceleracao'] = alucel['aumento'].diff()

#Merging the graphs in one image
fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    subplot_titles=[
        'Vendas Alucar 2017 e 2018',
        'Aumento das assinantes',
        'Aceleração de aumento de assinantes'
    ]
)

fig.add_trace(go.Scatter(x=alucel['dia'], y=alucel['vendas'], mode='lines', name='Vendas'), row=1, col=1)
fig.add_trace(go.Scatter(x=alucel['dia'], y=alucel['aumento'], mode='lines', name='Aumento'), row=2, col=1)
fig.add_trace(go.Scatter(x=alucel['dia'], y=alucel['aceleracao'], mode='lines', name='Aceleração'), row=3, col=1)

fig.update_layout(
    template='plotly_dark',  # Tema escuro
    height=900,  # Altura da figura
    title_text='Análise das Vendas Alucar de 2017 e 2018',  # Título geral
    title_x=0.5  # Centralizando o título
)

fig.show()

#Rolling avg
