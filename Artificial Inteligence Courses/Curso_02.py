'''
Atualmente, o escritório lida com uma grande quantidade de contratos, petições, jurisprudências e outros documentos legais, mas não existe uma forma eficiente de extrair essas informações críticas de forma automática, como, por exemplo:

Partes de pessoas envolvidas;
Datas relevantes;
Dispositivos legais citados.

Objetivo: Desenvolver um modelo de NLP especializado no reconhecimento de entidades nomeadas (NER).
Esse modelo será capaz de identificar e classificar automaticamente informações relevantes em textos jurídicos,
como partes envolvidas, datas e dispositivos legais.
'''
#%% Class 01 - Identifying basic entities
#%% Libraries
import zipfile 
import spacy
import pt_core_news_sm
import en_core_web_sm
import pandas as pd
import spacy.displacy
import random
from tqdm import tqdm
from spacy.training import Example
import shutil


#%% Reading name of all files
with zipfile.ZipFile('dados/texts.zip','r') as zip:
    for item in zip.namelist():
        print(item)

#%% Opening and reading a specific file 
with zipfile.ZipFile('dados/texts.zip','r') as zip:
    with zip.open(zip.namelist()[0]) as file:
        text = file.read().decode('utf-8')
        print(text)

#%% Loading Model and getting the entitites
model_ner = pt_core_news_sm.load()
doc = model_ner(text)
for entity in doc.ents:
    print(f'{entity.text} -> {entity.label_}')

#%% Creating a dataframe with entities
entities = []
labels = []

for entity in doc.ents:
    entities.append(entity.text)
    labels.append(entity.label_)

df = pd.DataFrame({'entities':entities, 'labels':labels})
df

#%% Showing the labels and the labels in the text with a ready model
model_labels = list(model_ner.get_pipe('ner').labels)
for item in model_labels:
    print(f'{item} - {spacy.explain(item)}')

spacy.displacy.render(doc, style='ent', jupyter=True)

#%% Ready Model in english
model_ner_eng = spacy.load('en_core_web_sm')
model_eng_labels = list(model_ner_eng.get_pipe('ner').labels)
for item in model_eng_labels:
    print(f'{item} - {spacy.explain(item)}')

spacy.displacy.render(doc, style='ent', jupyter=True)



#%% Class 02 - Gathering Data for training
#%% Tokenizing data
data = []
with zipfile.ZipFile('dados/texts.zip','r') as zip:
    for file_name in zip.namelist():
        with zip.open(file_name) as file:
            text = file.read().decode('utf-8')
            words = text.split()
            for word in words:
                data.append([file_name, word])

data_df = pd.DataFrame(data, columns=['filename','word'])
data_df.to_csv('words.csv', index=False, sep='\t')

#%% Getting tokenized file 
table_with_words_tokenized = pd.read_csv('dados/palavras_IOB.tsv', sep='\t')
#table_with_words_tokenized
table_with_words_tokenized.label.unique()

#%% Transforming data to spacy format 
file_group = table_with_words_tokenized.groupby(by='arquivo') #must be the name of the dataframe column
file_group.get_group(zip.namelist()[0])

#%% Extracting text and labels
#The labels of interest are the labels with prefix B and I
grouped_table = file_group.get_group('ADI2TJDFT.txt')[['palavra', 'label']].values
grouped_table
#%%
content = ''
annotations = {'entities':[]}

start_word = 0
end_word = 0 
for text, label in grouped_table:
    text = str(text)
    len_text = len(text)+1

    start_word = end_word
    end_word = start_word + len_text
    
    if label != 'O':
        annotation = (start_word, end_word-1, label)
        annotations['entities'].append(annotation)

    content = content + text + ' '

content
annotations
content.find('Conselho Especial')
#%% Extracting text and labels for all documents
#The labels of interest are the labels with prefix B and I
documents = []
files = file_group.groups.keys() #List of every file

#For each file, do the loop again
for file in files:
    document = []
    grouped_table = file_group.get_group(file)[['palavra', 'label']].values
    content = ''
    annotations = {'entities':[]}

    start_word = 0
    end_word = 0 
    for text, label in grouped_table:
        text = str(text)
        len_text = len(text)+1

        start_word = end_word
        end_word = start_word + len_text
        
        if label != 'O':
            annotation = (start_word, end_word-1, label)
            annotations['entities'].append(annotation)

        content = content + text + ' '
    document = (content, annotations)
    documents.append(document)

#For each document we will have the text and the coordinate with each word
#and the respective classification (only words with classification different of 'O'
#will be considered.
documents 

#%% Class 03 - Creating function for model training

#%% Spliting training and testing data
random.shuffle(documents)
training_data = documents[:len(documents)-10]
test_data = documents[len(documents)-10:]

#%% Building a function to train the model 
def treinar_modelo_ner(dados_treino, dados_validacao, epocas):

    modelo = spacy.load('pt_core_news_sm')

    if 'ner' not in modelo.pipe_names:
        ner = modelo.create_pipe('ner')
        modelo.add_pipe(ner, last = True)
    else:
        ner = modelo.get_pipe('ner')

    for _, anotacoes in dados_treino:
        for ent in anotacoes.get('entities'):
            ner.add_label(ent[2])

    outros_pipelines = [pipeline for pipeline in modelo.pipe_names if pipeline != 'ner']

    with modelo.disable_pipes(*outros_pipelines):
        spacy.util.fix_random_seed()
        otimizador = modelo.create_optimizer()

        for epoca in tqdm(range(epocas), desc = 'Treinando o modelo'):

            random.seed(10)
            random.shuffle(dados_treino)
            losses = {'ner': 0.0}

            for textos, anotacoes in dados_treino:
                exemplo = Example.from_dict(modelo.make_doc(textos), anotacoes)

                modelo.update([exemplo], drop = 0.2, sgd = otimizador, losses = losses)

            print(f'\nÉpoca {epoca+1} - Loss médio de treino: {losses["ner"]/len(dados_treino)}')

            val_losses = {'ner': 0.0}
            exemplos = []

            for textos, anotacoes in dados_validacao:
                exemplo = Example.from_dict(modelo.make_doc(textos), anotacoes)
                exemplos.append(exemplo)

            for exemplo in exemplos:

                modelo.update([exemplo], sgd = None, drop = 0, losses = val_losses)

            print(f'\nÉpoca {epoca+1} - Loss médio de validação: {val_losses["ner"]/len(dados_validacao)}')

    return modelo

#%% Class 04 - Applying NER model
#%% Training and saving model
model_ner = treinar_modelo_ner(training_data, test_data, 30)
model_ner.to_disk('modelos/model_ner')

arquivo_zip = 'modelos/model_ner.zip'
diretorio_modelo = 'modelos/model_ner'

# Compactar o diretório em um arquivo ZIP
shutil.make_archive(base_name=arquivo_zip.replace('.zip', ''), format='zip', root_dir=diretorio_modelo)

#%% Loading and testing model 
modelo_ner = spacy.load('modelos/model_ner')
doc = model_ner('João nasceu no dia 10/04/2015 em Florianópolis.')
for entity in doc.ents:
    print(f'{entity.text} -> {entity.label_}')

spacy.displacy.render(doc, style='ent', jupyter=True)

#%% Testing for a juridic document
with open('dados/20150110436469APC.txt', encoding='utf-8') as file:
    text = file.read()
    doc = model_ner(text)
    for entity in doc.ents:
        print(f'{entity.text} -> {entity.label_}')
    
    spacy.displacy.render(doc, style='ent', jupyter=True)

#%% Changing colors
labels = list(model_ner.get_pipe('ner').labels)
colors = {
'B-JURISPRUDENCIA': '#F0F8FF',
 'B-LEGISLACAO': '#FA8072',
 'B-LOCAL': '#98FB98',
 'B-ORGANIZACAO': '#DDA0DD',
 'B-PESSOA': '#F0E68C',
 'B-TEMPO': '#FFB6C1',
 'I-JURISPRUDENCIA': '#F0F8FF',
 'I-LEGISLACAO': '#FA8072',
 'I-LOCAL': '#98FB98',
 'I-ORGANIZACAO': '#DDA0DD',
 'I-PESSOA': '#F0E68C',
 'I-TEMPO': '#FFB6C1',
 'LOC': '#D3D3D3',
 'MISC': '#D3D3D3',
 'ORG': '#D3D3D3',
 'PER': '#D3D3D3'
}

options = {
    "ents": labels,
    "colors": colors
}
spacy.displacy.render(doc, style = 'ent', jupyter = True, options = options)