#%% Class 01 - Data Science: Dados e Visualizações
#%% Import Libraries
import numpy as np 
import pandas as pd 
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt 

#%% Read data
files = ['links.csv', 'movies.csv', 'ratings.csv', 'tags.csv']
data = pd.read_csv(f"..\\Data\\DS01 - Data Science analise - analise e visualizações de dados\\{files[2]}", delimiter=',')

#Get some information about the dataframe
avg_rating = round(data['rating'].mean(),2)
data['rating'].value_counts(), f"AVG Rate: {avg_rating}"
data.rating.describe().round(2)
data
#%% Histogram visualization
fig = px.histogram(data, x='rating',
                   title=f"Ratings Distribution (AVG Rage: {avg_rating})",
                   color_discrete_sequence=['#636EFA'])   

fig.update_layout(
    template='plotly_dark',  # Dark sci-fi style
    title_x=0.5,
    bargap=0.1  # Reduce space between bars
)

fig.show()

#%% Boxplot visualization
fig = px.box(data, x='rating',
                   title=f"Ratings Distribution (AVG Rage: {avg_rating})",
                   color_discrete_sequence=['#636EFA'])   

fig.update_layout(
    template='plotly_dark',  # Dark sci-fi style
    title_x=0.5,
    bargap=0.1  # Reduce space between bars
)

fig.show()





#%% Class 02 - Análise Exploratória
data_movies = pd.read_csv(f"..\\Data\\DS01 - Data Science analise - analise e visualizações de dados\\{files[1]}", delimiter=',')
data_movies[data_movies.movieId == 1]
#%% AVG per movie
avg_rating_per_movie = data.groupby('movieId').mean()[['rating']].round(2)
avg_rating_per_movie

#%% Histogram visualization
fig = px.histogram(avg_rating_per_movie, x='rating',
                   title=f"Ratings Distribution (AVG Rage: {avg_rating})",
                   color_discrete_sequence=['#636EFA'],
                    nbins=10)   
fig.update_layout(
    template='plotly_dark',  # Dark sci-fi style
    title_x=0.5,
    bargap=0.1  # Reduce space between bars
)
fig.show()







#%% Class 03 - Variaveis
#%% Class 04 - Visualização de dados
data_tmdb = pd.read_csv(f"..\\Data\\DS01 - Data Science analise - analise e visualizações de dados\\tmdb_5000_movies.csv", delimiter=',')
data_tmdb[['original_language']].value_counts().to_frame() #to_frame transforma em dataframe
#data_tmdb[['original_language']].value_counts().reset_index() #reset_index para resetar o index
language_count = data_tmdb[['original_language']].value_counts().reset_index() 

#%% Ploting categorical plots
sns.barplot(x="original_language", y="count", data=language_count)

#without need of use value count
sns.catplot(x='original_language', data=data_tmdb, kind="count")

#%%
#Ploting with plotly
fig = px.bar(language_count, x='original_language', y='count', 
             title='Contagem de Idiomas Originais',
             labels={'original_language': 'Idioma Original', 'count': 'Contagem'},
             color='count', color_continuous_scale='Blues')

fig.update_layout(
    template='plotly_dark',  # Dark sci-fi style
    title_x=0.5,
    bargap=0.1,  # Reduce space between bars
    yaxis_type="log" #Put a logaritmic scale
)

fig.show()

#%% Using pie chart and comparing english data with all rest combined
total_language_count = language_count['count'].sum()
english_language_count = language_count['count'].loc[0]
others_language_count = total_language_count - english_language_count
print(english_language_count, others_language_count)

#Assembling new dataframe
data = {
    'language': ['english', 'others'],
    'total': [english_language_count, others_language_count]
}
formatted_data = pd.DataFrame(data)
formatted_data

#Ploting with plotly
fig = px.pie(formatted_data, names='language', values='total', 
             title='Original Language Count')

fig.update_layout(
    template='plotly_dark',  # Dark sci-fi style
    title_x=0.5)

fig.show()


#%% Movies with other languages then english 
data_other_languages = data_tmdb.query("original_language != 'en'")[['original_language']].value_counts().reset_index()
data_other_languages.columns = ['original_language', 'count']
data_other_languages = pd.DataFrame(data_other_languages)
data_other_languages




#%% Barplot with plotly
fig = px.bar(data_other_languages, x='original_language', y='count', 
             title='Contagem de Idiomas Originais',
             labels={'original_language': 'Idioma Original', 'count': 'Contagem'},
             color='count', color_continuous_scale='Blues')

fig.update_layout(
    template='plotly_dark',
    title_x=0.5,           
    bargap=0.1,         
    yaxis_type="log"    
)
fig.show()