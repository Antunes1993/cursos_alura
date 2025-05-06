#%% Class 01 - Analisando o tipo de dado.

# Import Libraries
import numpy as np 
import pandas as pd 

data = pd.read_csv("..\\Data\\DS02 - Estatística com Python - Frequências e Medidas\\dados.csv", delimiter=',')
data.head()

#Variaveis qualitativas ordinais 
#variaveis que podem ser ordenadas ou hierarquizadas. 
sorted(data['Anos de Estudo'].unique())

#Variaveis qualitativas nominais
#Variaveis que não podem ser ordenadas ou hierarquizadas
sorted(data['UF'].unique())
sorted(data['Sexo'].unique())   
sorted(data['Cor'].unique())   

#Variaveis quantitativas discretas 
#Variaveis que representam uma contagem onde os valores possívels formam um conjunto
sorted(data['Idade'].unique())   

#Observação:
#A variavel idade pode ser classificada de três formas distintas:
# 1. Quantitativa Discreta - quando representa anos completos (números inteiros)
# 2. Quantitativa Contínua - quando representa a idade exata, sendo representado por uma fração do ano. 
# 3. Qualitativa Ordinal - quando representa faixas de idade.
