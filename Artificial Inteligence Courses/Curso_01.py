#%% Libraries
###########################################  Class 01  ##########################################
import pandas as pd 
import unidecode
import seaborn as sns
import matplotlib.pyplot as plt
#%% Gathering Data
#################################################################################################
data = pd.read_csv('dados/dataset_avaliacoes.csv')
data.head()
data.value_counts('sentimento') #Binary classification (positive and negative)
print(f"1°st Review: {data.iloc[0,1]}")
print(f"2°st Review: {data.iloc[1,1]}")


#################################################################################################
#Bag of words 
#Calculate the frequency of each word in the string. 
from sklearn.feature_extraction.text import CountVectorizer 

#Simple Example
example_text = ['Comprei um produto ótimo', 'Comprei um produto ruim']
vectorizer = CountVectorizer(lowercase=False)
bag_of_words = vectorizer.fit_transform(example_text)
sparse_matrix = pd.DataFrame.sparse.from_spmatrix(bag_of_words, columns=vectorizer.get_feature_names_out())
sparse_matrix
#%% Bag of words applied in the dataset 
vectorizer = CountVectorizer(lowercase=False)
bag_of_words = vectorizer.fit_transform(data.avaliacao)
sparse_matrix_reviews = pd.DataFrame.sparse.from_spmatrix(bag_of_words, columns=vectorizer.get_feature_names_out())
sparse_matrix_reviews
#%% Simple classifier with logistic regression 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LogisticRegression 

def logistic_regression_classifier(data, bag_of_words):
    X_train, X_test, y_train, y_test = train_test_split(bag_of_words, data.sentimento, test_size=0.3, random_state=42)
    logistic_regression = LogisticRegression()
    logistic_regression.fit(X_train, y_train)
    accuracy_score = round(logistic_regression.score(X_test, y_test), 2)
    return accuracy_score

acuracia = logistic_regression_classifier(data, bag_of_words)
print(f"Accuracy: {acuracia}")










#%%  ###########################################  Class 02  ##########################################
#%% WordCloud 
#WordCloud is a technique to visualize the most frequent words in a text.
from wordcloud import WordCloud

all_words_from_reviews = ' '.join([text for text in data.avaliacao])
word_cloud = WordCloud().generate(all_words_from_reviews)
plt.figure(figsize=(20,7))
plt.axis('off')
plt.imshow(word_cloud, interpolation='bilinear')

#To paint words individually
word_cloud = WordCloud(collocations=False).generate(all_words_from_reviews)
plt.figure(figsize=(20,7))
plt.axis('off')
plt.imshow(word_cloud, interpolation='bilinear')

#WordCloud with positive and negative reviews
def word_cloud_segmented_by_sentiment(text, text_column, sentiment):
    text_sentiment = text.query(f'sentimento == "{sentiment}"')[text_column]
    text_united = ' '.join([text for text in text_sentiment])
    word_cloud = WordCloud(collocations=False).generate(text_united)
    plt.figure(figsize=(20,7))
    plt.axis('off')
    plt.imshow(word_cloud, interpolation='bilinear')

word_cloud_segmented_by_sentiment(data, 'avaliacao', 'negativo')
#%% Tokenization
#Tokenization is the process of breaking down a text into words or sentences.
import nltk
from nltk import tokenize
nltk.download('all')

#Example of tokenization
frases = ['um produto bom', 'um produto ruim']
frequency = nltk.FreqDist(frases)
frequency

#Example of tokenization using spaces
frase = 'O produto é excelente e a entrega foi muito rápida.'
token_whitespace = tokenize.WhitespaceTokenizer() #Tokenization by spaces
token_frase = token_whitespace.tokenize(frase)
print(token_frase)

#White Space Tokenization applied to the dataset reviews
token_words_column_reviews = token_whitespace.tokenize(all_words_from_reviews)
frequency_token_words_column_reviews = nltk.FreqDist(token_words_column_reviews)
frequency_token_words_column_reviews

#Converting to a dataframe to better view 
data_frequency_tokenized_words_column_reviews = pd.DataFrame({'Word': list(frequency_token_words_column_reviews.keys()), 'Frequency': list(frequency_token_words_column_reviews.values())}) 
data_frequency_tokenized_words_column_reviews.head()

#Selecting the 20 most frequent words
data_frequency_tokenized_words_column_reviews = data_frequency_tokenized_words_column_reviews.nlargest(columns='Frequency', n=20)
data_frequency_tokenized_words_column_reviews

#Plotting the 20 most frequent words
plt.figure(figsize=(20,7))
sns.barplot(data=data_frequency_tokenized_words_column_reviews, x='Word', y='Frequency')


#%% ###########################################  Class 03  ##########################################
#In the graph of the last class we realize the need of a pre-processing step to remove the stopwords, 
#which are irrelevant words for the analysis.
#Keep the stop words will make the analysis less acurate and enlarge the model dimensions. 

#%% Removing stopwords
stopwords = nltk.corpus.stopwords.words('portuguese')
processed_words = []

for item in data.avaliacao:
    tokenized_words_white_space = token_whitespace.tokenize(item)
    new_phrase = [word for word in tokenized_words_white_space if word.lower() not in stopwords]
    processed_words.append(' '.join(new_phrase))

data['tratamento_1'] = processed_words
data.head()

#%% Classification without stopwords
def logistic_regression_classifier(data, text_column, classification_column):
    vectorizer = CountVectorizer(lowercase=False)
    bag_of_words = vectorizer.fit_transform(data[text_column])
    X_train, X_test, y_train, y_test = train_test_split(bag_of_words, data[classification_column], test_size=0.3, random_state=42)
    logistic_regression = LogisticRegression()
    logistic_regression.fit(X_train, y_train)
    accuracy_score = round(logistic_regression.score(X_test, y_test), 2)
    return accuracy_score

acuracia = logistic_regression_classifier(data, 'tratamento_1', 'sentimento')
print(f"Accuracy: {acuracia}")

## 
#New frequency graph without stop words
def frequency_graph(data, text_column, quantity):
    all_words_from_reviews = ' '.join([text for text in data[text_column]])
    space_token = tokenize.WhitespaceTokenizer()
    frequency = nltk.FreqDist(space_token.tokenize(all_words_from_reviews))
    data_frequency = pd.DataFrame({'Word': list(frequency.keys()), 'Frequency': list(frequency.values())})
    data_frequency = data_frequency.nlargest(columns='Frequency', n=quantity)
    plt.figure(figsize=(20,7))
    sns.barplot(data=data_frequency, x='Word', y='Frequency')
    plt.show()

frequency_graph(data, 'tratamento_1', 20)


#%% Adding a Tokenization step to remove punctuation 
#Example of tokenization using punctuation
frases = ['Esse smartphone superou expectativas, recomendo.']
frequency = nltk.FreqDist(frases)

token_punctuation = tokenize.WordPunctTokenizer()
tokenized_phrase = token_punctuation.tokenize(frases[0])
print(tokenized_phrase)

#Tokenization of column 'avaliacao'
all_words_from_reviews = ' '.join([text for text in data.avaliacao])
token_words_column_reviews = token_punctuation.tokenize(all_words_from_reviews)
frequency_token_words_column_reviews = nltk.FreqDist(token_words_column_reviews)
frequency_token_words_column_reviews

#Tokenization of column 'tratamento_1'
all_words_from_reviews_white_space_tokenized = ' '.join([text for text in data.tratamento_1])
token_words_column_reviews = token_punctuation.tokenize(all_words_from_reviews_white_space_tokenized)
frequency_token_words_column_reviews = nltk.FreqDist(token_words_column_reviews)
frequency_token_words_column_reviews

#Converting to a dataframe to better view 
data_frequency_tokenized_words_column_reviews = pd.DataFrame({'Word': list(frequency_token_words_column_reviews.keys()), 'Frequency': list(frequency_token_words_column_reviews.values())}) 
data_frequency_tokenized_words_column_reviews.head()

#Selecting the 20 most frequent words
data_frequency_tokenized_words_column_reviews = data_frequency_tokenized_words_column_reviews.nlargest(columns='Frequency', n=20)
data_frequency_tokenized_words_column_reviews

#Plotting the 20 most frequent words
plt.figure(figsize=(20,7))
sns.barplot(data=data_frequency_tokenized_words_column_reviews, x='Word', y='Frequency')

#%% Removing punctuation from the dataset.tratamento_1
processed_words = []
for item in data.tratamento_1:
    text_words = token_punctuation.tokenize(item)
    new_phrase = [word for word in text_words if word.isalpha()]
    processed_words.append(' '.join(new_phrase))
    
data['tratamento_2'] = processed_words
data.head()

#frequency_graph(data, 'tratamento_2', 20)

#%% Removing accentuation from the dataset.tratamento_2
#Example of removing accentuation from string
phrase = 'O produto é excelente e a entrega foi muito rápida.'
test = unidecode.unidecode(phrase)
test

#Removing accentuation and stop wordsfrom the dataset.tratamento_2
without_accentuation = [unidecode.unidecode(item) for item in data.tratamento_2] #Removing accentuation
stopwords_without_accentuation = [unidecode.unidecode(text) for text in stopwords] #Removing accentuation from stopwords

data['tratamento_3'] = without_accentuation
processed_words = []
for item in data['tratamento_3']:
    tokenized_words = token_punctuation.tokenize(item)
    new_phrase = [word for word in tokenized_words if word not in stopwords_without_accentuation]
    processed_words.append(' '.join(new_phrase))

data['tratamento_3'] = processed_words
data.head()
frequency_graph(data, 'tratamento_3', 20)
#%% Treating capitalized words
#Example of treating capitalized words
phrase = 'O Produto é excelente e a entrega foi muito rápida.'
phrase = phrase.lower()
print(phrase)


#Treating capitalized words in the dataset.tratamento_3
processed_words = []
for item in data['tratamento_3']:
    item = item.lower()
    tokenized_words = token_punctuation.tokenize(item)
    new_frase = [word for word in tokenized_words if word not in stopwords_without_accentuation]
    processed_words.append(' '.join(new_frase))


data['tratamento_4'] = processed_words
data.head()
frequency_graph(data, 'tratamento_4', 20)

#Checking if the model accuracy improved
acuracia = logistic_regression_classifier(data, 'tratamento_4', 'sentimento')
acuracia


#%% ###########################################  Class 04  ##########################################
#%% Simplifying the words with the stemming technique
# Example of stemming
stemmer = nltk.RSLPStemmer()
stemmer.stem('gostado')

# Stemming applied to the dataset.tratamento_4
processed_words = [] 
for item in data.tratamento_4:
    text_words = token_punctuation.tokenize(item)
    new_phrase= [stemmer.stem(item) for item in text_words]
    processed_words.append(' '.join(new_phrase))

data['tratamento_5'] = processed_words
data.head()

#TF-IDF - Term Frequency-Inverse Document Frequency
#TF-IDF is a technique to evaluate the importance of a word in a text.
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer_tfidf = TfidfVectorizer(lowercase=False, max_features=50)

#Applying TF-IDF to the dataset.avaliacao
tfidf_raw = vectorizer_tfidf.fit_transform(data.avaliacao)
X_train, X_test, y_train, y_test = train_test_split(tfidf_raw, data.sentimento, test_size=0.3, random_state=42)
logistic_regression = LogisticRegression()
logistic_regression.fit(X_train, y_train)
accuracy_score = round(logistic_regression.score(X_test, y_test), 2)
accuracy_score

#Applying TF-IDF to the dataset.tratamento_5
tfidf_5 = vectorizer_tfidf.fit_transform(data.tratamento_5)
X_train, X_test, y_train, y_test = train_test_split(tfidf_5, data.sentimento, test_size=0.3, random_state=42)
logistic_regression = LogisticRegression()
logistic_regression.fit(X_train, y_train)
accuracy_score = round(logistic_regression.score(X_test, y_test), 2)
accuracy_score

#%% #Gathering Context from phrases
from nltk import ngrams 
phrase = 'Comprei um produto ótimo.'
tokenized_phrase = token_whitespace.tokenize(phrase)
pairs = ngrams(tokenized_phrase, 2)
print(list(pairs))

#Gathering context from the dataset.tratamento_5
vectorizer_tfidf = TfidfVectorizer(lowercase=False, max_features=1000, ngram_range=(1,2))
tfidf_1000 = vectorizer_tfidf.fit_transform(data.tratamento_5)
X_train, X_test, y_train, y_test = train_test_split(tfidf_1000, data.sentimento, test_size=0.3, random_state=42)
logistic_regression = LogisticRegression()
logistic_regression.fit(X_train, y_train)
accuracy_score = round(logistic_regression.score(X_test, y_test), 2)
accuracy_score

#%% ###########################################  Class 05  ##########################################
#%% Saving the model and the vectorizer 
import joblib 
joblib.dump(logistic_regression, 'model_logistic_regression.pkl')
joblib.dump(vectorizer_tfidf, 'tdidf_vectorizer.pkl')

#%% Loading model 
tfidf = joblib.load('tdidf_vectorizer.pkl')
model = joblib.load('model_logistic_regression.pkl')

#%% Creating a new function to process new data
stopwords = nltk.corpus.stopwords.words('portuguese')
token_punctuation = tokenize.WordPunctTokenizer()
stemmer = nltk.RSLPStemmer()

def process_reviews(new_data):
    #Step1 - Tokenization
    tokens = token_punctuation.tokenize(new_data)
    #Step2 - Convert words to lowcase 
    processed_phrase = [word.lower() for word in tokens if word.isalpha()]
    #Step3 - Remove stopwords
    processed_phrase = [word for word in processed_phrase if word not in stopwords]
    #Step4 - Remove accentuation
    processed_phrase = [unidecode.unidecode(word) for word in processed_phrase]
    #Step5 - Stemming
    processed_phrase = [stemmer.stem(word) for word in processed_phrase] #stemming automatically convert to lower
    #Step6 - Joining the words
    processed_phrase = ' '.join(processed_phrase)

    return processed_phrase


new_review = ["Ótimo produto, super recomendo!",
            "A entrega atrasou muito! Estou decepcionado com a compra",
            "Muito satisfeito com a compra. Além de ter atendido as expectativas, o preço foi ótimo",
            "Horrível!!! O produto chegou danificado e agora estou tentando fazer a devolução.",
            '''Rastreando o pacote, achei que não fosse recebê-lo, pois, na data prevista, estava sendo entregue em outra cidade.
            Mas, no fim, deu tudo certo e recebi o produto.Produto de ótima qualidade, atendendo bem as minhas necessidades e por
            um preço super em conta.Recomendo.''']

new_processed_reviews = [process_reviews(item) for item in new_review]  
new_reviews_tfidf = tfidf.transform(new_processed_reviews)
predictions = model.predict(new_reviews_tfidf)
data_predictions = pd.DataFrame({'Review': new_review, 'Sentiment': predictions})
data_predictions