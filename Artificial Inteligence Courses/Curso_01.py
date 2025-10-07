#%% Libraries
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Curso 01 - NLP:Aplicando processamento de linguagem natural para análise de 
# sentimentos.
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import pandas as pd 
import unidecode
import seaborn as sns
import matplotlib.pyplot as plt
#%% Gathering Data
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
data = pd.read_csv('dados/dataset_avaliacoes.csv')
data.head()

#%%
#Analise preliminar do dataset 
#-----------------------------------------------------------------------
data.value_counts('sentimento')
index=2

print(f"Sentimento: {data.sentimento[index]}")
print(f"Avaliação: {data.avaliacao[index]}")

#%%
#Convertendo texto em algo numerico. 
######################################################################################
# Tecnica 01 - BAG OF WORDS 
######################################################################################
# Obtenção de vetor com numeros de acordo com a frequencia de uma palavra em um texto. 
from sklearn.feature_extraction.text import CountVectorizer 
texto = ['Esse produto é ótimo.', 'Esse produto é péssimo.']
vetorizer  = CountVectorizer() 
bag_of_words = vetorizer.fit_transform(texto)
bag_of_words #Matriz esparsa. 

#Visualizando a matriz esparsa
matriz_esparsa = pd.DataFrame.sparse.from_spmatrix(bag_of_words, columns=vetorizer.get_feature_names_out())
matriz_esparsa


#%%
#Fazendo o mesmo para nosso dataframe
vetorizer  = CountVectorizer(lowercase=False) 
bag_of_words_dataset = vetorizer.fit_transform(data.avaliacao)
matriz_esparsa = pd.DataFrame.sparse.from_spmatrix(bag_of_words_dataset, columns=vetorizer.get_feature_names_out())
matriz_esparsa

#Vemos que estamos com uma matriz esparsa muito grande. 
#Para otimizar processamento vamos usar uma tecnica difretne.
n=50
vetorizer  = CountVectorizer(lowercase=False, max_features=n) #Pega as n palavras mais frequentes. 
bag_of_words_dataset = vetorizer.fit_transform(data.avaliacao)
matriz_esparsa = pd.DataFrame.sparse.from_spmatrix(bag_of_words_dataset, columns=vetorizer.get_feature_names_out())
matriz_esparsa

#%%
#Classificando os sentimentos - Treinamento e teste do modelo 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LogisticRegression

x_treino, x_teste, y_treino, y_teste = train_test_split(bag_of_words_dataset, data.sentimento, random_state=5)
regressao_logistica = LogisticRegression()

regressao_logistica.fit(x_treino, y_treino)
acc = regressao_logistica.score(x_teste, y_teste)
f"{round(acc*100, 2)}%"



#%% #Visualizando palavras mais frequentes com wordcloud. 
from wordcloud import WordCloud
todas_palavras = [item for item in data.avaliacao]
todas_palavras = ' '.join([texto for texto in data.avaliacao])
nuvem_palavras = WordCloud(width=800, height=500, max_font_size=110).generate(todas_palavras)



import matplotlib.pyplot as plt 
plt.figure()
plt.imshow(nuvem_palavras, interpolation='bilinear')
plt.axis('off')

#%%
def nuvem_words(dataframe, coluna, sentimento):
    import matplotlib.pyplot as plt 
    from wordcloud import WordCloud
    data_filtrada = dataframe.query(f"{coluna} == '{sentimento}'")
    todas_palavras = ' '.join([texto for texto in data_filtrada.avaliacao])
    nuvem_palavras = WordCloud(width=800, height=500, max_font_size=110).generate(todas_palavras)
    plt.figure()
    plt.imshow(nuvem_palavras, interpolation='bilinear')
    plt.axis('off')

nuvem_words(data, "sentimento", "negativo")
nuvem_words(data, "sentimento", "positivo")

#%%
######################################################################################
# Tecnica 02 - TOKENIZAÇÃO

# 1. Tokenização considerando espaços em branco. WhitespaceTokenizer
# 2. Remoção de stop words nltk.corpus.stopwords.words('portuguese')
# 3. Remoção de pontuação WordPunctTokenizer
# 4. Removendo acentuação
# 5. Uniformizando o texto
######################################################################################
import nltk 
from nltk import tokenize 

nltk.download('all')
frases = ['Um produto bom.', 'Um produto ruim']
frequencia = nltk.FreqDist(frases)
frequencia

#%%
#Tokeninzando uma a partir das palavras que estao contidas na frase.
frase = 'O produto é excelente e a entrega foi muito rápida! O entregador foi muito eficiente.'
token_espaco = tokenize.WhitespaceTokenizer()
token_frase = token_espaco.tokenize(frase)
token_frase

#Calculando a frequencia das palavras na frase 
frequencia = nltk.FreqDist(token_frase)
df_frequencia = pd.DataFrame({'Palavra':list(frequencia.keys()),
                              'Frequencia':list(frequencia.values())})

#Vendo as palavras mais frequentes.
df_frequencia.nlargest(columns='Frequencia', n=10)

#Aplicando a tokenização de palavras dataframe
data = pd.read_csv('dados/dataset_avaliacoes.csv')
todas_palavras = [item for item in data.avaliacao]
todas_palavras = ' '.join([texto for texto in data.avaliacao])
token_frase = token_espaco.tokenize(todas_palavras)

frequencia = nltk.FreqDist(token_frase)
df_frequencia = pd.DataFrame({'Palavra':list(frequencia.keys()),
                              'Frequencia':list(frequencia.values())})

#Vendo as palavras mais frequentes.
df_frequencia.nlargest(columns='Frequencia', n=10)


#%%
# Limpando e normalizando dados textuais. 

# Removendo stop words (palavras sem valor semântico) 
palavras_irrelevantes = nltk.corpus.stopwords.words('portuguese')
palavras_irrelevantes


token_espaco = tokenize.WhitespaceTokenizer()
frase_processada = []

for frase in data.avaliacao:
    palavras_texto = token_espaco.tokenize(frase)
    nova_frase = [palavra for palavra in palavras_texto if palavra not in palavras_irrelevantes]
    frase_processada.append(' '.join(nova_frase))

data['tratamento_01'] = frase_processada
data.head()

#%%
#Verificando se o modelo treinado sem stop-words está melhor
n=50
vetorizer  = CountVectorizer(lowercase=False, max_features=n) #Pega as n palavras mais frequentes. 
bag_of_words_dataset = vetorizer.fit_transform(data.tratamento_01)
x_treino, x_teste, y_treino, y_teste = train_test_split(bag_of_words_dataset, data.sentimento, random_state=5)
regressao_logistica = LogisticRegression()

regressao_logistica.fit(x_treino, y_treino)
acc = regressao_logistica.score(x_teste, y_teste)
f"{round(acc*100, 2)}%"



#%%
# Removendo pontuação
token_pontuacao = tokenize.WordPunctTokenizer()
frase_processada = []

for frase in data.tratamento_01:
    palavras_texto = token_pontuacao.tokenize(frase)
    nova_frase = [palavra for palavra in palavras_texto if palavra.isalpha() and palavra not in palavras_irrelevantes]
    frase_processada.append(' '.join(nova_frase))


data['tratamento_02'] = frase_processada
data.head()

#%%
#Removendo acentuação 
import unidecode 

sem_acentos = [unidecode.unidecode(texto) for texto in data['tratamento_02']]
stopwords_sem_acento = [unidecode.unidecode(texto) for texto in palavras_irrelevantes]


data['tratamento_3'] = sem_acentos

frase_processada = []

for opiniao in data['tratamento_3']:
    palavras_texto = token_pontuacao.tokenize(opiniao)
    nova_frase = [palavra for palavra in palavras_texto if palavra not in stopwords_sem_acento]
    frase_processada.append(' '.join(nova_frase))

data['tratamento_3'] = frase_processada

#%%
#Transformando tudo em lower case
frase_processada = []

for opiniao in data['tratamento_3']:
    opiniao = opiniao.lower()
    palavras_texto = token_pontuacao.tokenize(opiniao)
    nova_frase = [palavra for palavra in palavras_texto if palavra not in stopwords_sem_acento]
    frase_processada.append(' '.join(nova_frase))

data['tratamento_04'] = frase_processada


#%% Aplicando novamente o modelo
n=50
vetorizer  = CountVectorizer(lowercase=False, max_features=n) #Pega as n palavras mais frequentes. 
bag_of_words_dataset = vetorizer.fit_transform(data.tratamento_04)
x_treino, x_teste, y_treino, y_teste = train_test_split(bag_of_words_dataset, data.sentimento, random_state=5)
regressao_logistica = LogisticRegression()

regressao_logistica.fit(x_treino, y_treino)
acc = regressao_logistica.score(x_teste, y_teste)
f"{round(acc*100, 2)}%"




#%%
######################################################################################
# Tecnica 03 - STEMIZAÇÃO 
# 1. Redução da palavra ao seu radical. 
######################################################################################
df = data
stemmer = nltk.RSLPStemmer()
frase_processada = []
for opinion in df["tratamento_4"]:
    palavras_texto = token_pontuacao.tokenize(opinion)
    nova_frase = [stemmer.stem(palavra) for palavra in palavras_texto]
    frase_processada.append(" ".join(nova_frase))

df["tratamento_5"] = frase_processada



#%%
######################################################################################
# Tecnica 04 - TF-IDF
# 1. Aplicação de pesos as palavras
######################################################################################
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(lowercase=False, max_features=50)

tfidf_bruto = tfidf.fit_transform(df["avaliacao"])
X_treino, X_teste, y_treino, y_teste = train_test_split(tfidf_bruto, df["sentimento"], random_state=4978)
regressao_logistica.fit(x_treino, y_treino)
acuracia_tfidf_bruto = regressao_logistica.score(x_teste, y_teste)
print(f"Acurácia do modelo: {acuracia_tfidf_bruto *100:.2f}%")


tfidf_tratados = tfidf.fit_transform(df['tratamento_5'])
X_treino, X_teste, y_treino, y_teste = train_test_split(tfidf_tratados, df['sentimento'], random_state=4978)
regressao_logistica.fit(X_treino, y_treino)
acuracia_tfidf_tratados = regressao_logistica.score(X_teste, y_teste)
print(f'Acurácia do modelo: {acuracia_tfidf_tratados *100:.2f}%')


######################################################################################
# Tecnica 05 - N-GRAMS
# 1. Serve para captura de contexto entre as palavras.
######################################################################################
from nltk import ngrams
tfidf_50 = TfidfVectorizer(lowercase=False, max_features=400, ngram_range=(1,2))
vetor_tfidf = tfidf_50.fit_transform(df['tratamento_5'])
X_treino, X_teste, y_treino, y_teste = train_test_split(vetor_tfidf, df['sentimento'], random_state=4978)
regressao_logistica.fit(X_treino, y_treino)
acuracia_tfidf_ngrams = regressao_logistica.score(X_teste, y_teste)
print(f'Acurácia do modelo com 50 features e ngrams: {acuracia_tfidf_ngrams * 100:.2f}%')




######################################################################################
# Salvando modelo e vetorizador
######################################################################################
import joblib 
joblib.dump(tfidf, 'tfidf_vectorizer.pkl')
joblib.dump(regressao_logistica, 'modelo_regressao_logistica.pkl')